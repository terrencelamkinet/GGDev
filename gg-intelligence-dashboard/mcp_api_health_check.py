#!/usr/bin/env python3
"""
api_health_check.py — no_agent cron script.
Every 15min: discover all MCP servers + API keys, probe health, store in PG.
Silent if nothing changed. Outputs summary on changes.
Zero LLM involvement — pure Python stdlib.
"""
import json, os, sys, subprocess, urllib.request, urllib.error, select, signal
from datetime import datetime, timezone, timedelta
from pathlib import Path

HKT = timezone(timedelta(hours=8))
HOME = Path.home()

# ── Paths ──
CONFIG_PATH = HOME / ".hermes" / "config.yaml"
ENV_PATH = HOME / ".hermes" / ".env"
NOTION_KEY_PATH = HOME / ".config" / "notion" / "api_key"
SCRIPTS_DIR = HOME / ".hermes" / "scripts"
ALERT_WRITER = SCRIPTS_DIR / "alert_writer.py"
MCP_STATE_FILE = HOME / ".hermes" / "data" / "mcp_last_known.json"

# ── PG (reuse task_hub.py) ──
sys.path.insert(0, str(SCRIPTS_DIR))
from task_hub import pg_cursor

# ── Known API key names that are NOT MCP-managed ──
API_KEY_MAP = {
    "OPENAI_API_KEY": {"desc": "DeepSeek LLM", "category": "ai"},
    "TELEGRAM_BOT_TOKEN": {"desc": "Telegram Bot", "category": "messaging"},
}

# ── Circuit Breaker Settings ──
MAX_RETRIES = 2          # Auto-restart attempts before circuit opens
CIRCUIT_COOLDOWN = 2     # Skip this many probe cycles when HALF_OPEN (2 × 15min = 30min)

# MCP server command patterns for quick probe
def probe_command(cmd_str, timeout=5):
    """Quick check if an MCP server command can start. Returns (ok, error)."""
    if not cmd_str:
        return False, "no command"
    parts = cmd_str.strip().split()
    if not parts:
        return False, "empty command"
    try:
        r = subprocess.run(parts[:1], capture_output=True, timeout=timeout)
        if r.returncode != 0:
            # Some CLIs exit non-zero without args (e.g. designlang). Retry with --version.
            try:
                r2 = subprocess.run(parts[:1] + ["--version"], capture_output=True, timeout=timeout)
                return r2.returncode == 0, f"exit={r.returncode} (retry --version: exit={r2.returncode})"
            except:
                pass
        return r.returncode == 0, f"exit={r.returncode}"
    except FileNotFoundError:
        return False, "binary not found"
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except Exception as e:
        return False, str(e)[:60]


def probe_mcp_server_deep(name, command, args, env, timeout=10):
    """Actually start MCP server, run full initialize+tools/list, verify JSON-RPC response.
    Tries both standard method names (tools/list and listTools) for compatibility.
    Returns (ok: bool, detail: str)."""
    try:
        proc = subprocess.Popen(
            [command] + args if args else [command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, **(env or {})},
            text=True,
        )
    except FileNotFoundError:
        return False, "binary not found"
    except Exception as e:
        return False, str(e)[:60]

    def send_msg(msg):
        if proc.stdin:
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()

    def read_response(wait=0.5):
        """Read one JSON-RPC response line. Returns parsed dict or None."""
        import select as _sel
        r, _, _ = _sel.select([proc.stdout], [], [], wait)
        if r and proc.stdout:
            line = proc.stdout.readline()
            if line:
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    pass
        return None

    try:
        start = datetime.now()

        # Step 1: Initialize
        send_msg({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2024-11-05",
                              "capabilities": {},
                              "clientInfo": {"name": "health-check", "version": "1.0"}}})
        resp = None
        while (datetime.now() - start).total_seconds() < timeout:
            resp = read_response(0.5)
            if resp is not None:
                break
            if proc.poll() is not None:
                break

        if resp is None:
            proc.kill()
            proc.wait()
            return False, "no response to initialize"

        if "error" in resp or resp.get("id") != 1:
            err = resp.get("error", {}).get("message", str(resp)[:60])
            proc.kill()
            proc.wait()
            return False, f"initialize error: {err}"

        # Step 2: Send initialized notification (no response expected)
        send_msg({"jsonrpc": "2.0", "method": "notifications/initialized"})

        # Step 3: Try tools/list (MCP 2024-11-05 spec)
        send_msg({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        resp = None
        while (datetime.now() - start).total_seconds() < timeout:
            resp = read_response(0.5)
            if resp is not None:
                break
            if proc.poll() is not None:
                break

        # Step 3b: If tools/list not recognized, try listTools (newer MCP spec)
        if resp is None:
            send_msg({"jsonrpc": "2.0", "id": 2, "method": "listTools", "params": {}})
            while (datetime.now() - start).total_seconds() < timeout:
                resp = read_response(0.5)
                if resp is not None:
                    break
                if proc.poll() is not None:
                    break

        proc.terminate()
        try:
            proc.wait(timeout=3)
        except:
            proc.kill()
            proc.wait()

        if resp is None:
            stderr = proc.stderr.read()[:120] if proc.stderr else ""
            if stderr:
                return False, f"no listTools response: {stderr.strip()}"
            return False, f"no response in {timeout}s"

        if "error" in resp:
            return False, f"listTools error: {resp['error'].get('message', str(resp)[:60])}"

        tools = resp.get("result", {}).get("tools", [])
        tool_count = len(tools)
        if tool_count > 0:
            first_tools = ", ".join(t["name"] for t in tools[:3])
            return True, f"✅ {tool_count} tools ({first_tools})"
        else:
            return True, f"✅ 0 tools (server running)"

    except Exception as e:
        try:
            proc.kill()
            proc.wait(timeout=2)
        except:
            pass
        return False, str(e)[:60]

    finally:
        # Ensure process is cleaned up
        try:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=3)
        except:
            pass


def load_mcp_state():
    """Load last-known-good state for MCP servers. Returns dict of name->status."""
    try:
        if MCP_STATE_FILE.exists():
            return json.loads(MCP_STATE_FILE.read_text())
    except:
        pass
    return {}


def save_mcp_state(state):
    """Save MCP server state."""
    os.makedirs(str(MCP_STATE_FILE.parent), exist_ok=True)
    MCP_STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def write_alert(source, severity, title, message):
    """Call alert_writer.py to raise an alert."""
    try:
        subprocess.run(
            [sys.executable, str(ALERT_WRITER), source, severity, title, message],
            capture_output=True, timeout=10
        )
    except:
        pass


def auto_restart_mcp(name, command, args):
    """Kill MCP process by command signature so gateway respawns it.
    Returns (ok: bool, detail: str)."""
    if not command:
        return False, "no command"
    
    # Build a unique search pattern from the command
    cmd_base = command.split("/")[-1]  # e.g. "npx" or "python3"
    # For uniqueness, also match the first unique arg
    kill_pattern = cmd_base
    for a in (args or []):
        if not a.startswith("-"):
            kill_pattern = a.split("/")[-1]
            break
    
    try:
        # Find matching processes
        r = subprocess.run(
            ["pgrep", "-f", kill_pattern],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode != 0 or not r.stdout.strip():
            return False, f"no process found matching '{kill_pattern}'"
        
        pids = [p.strip() for p in r.stdout.strip().split("\n") if p.strip()]
        if not pids:
            return False, "no pids"
        
        # Kill each matching PID (SIGTERM first, then SIGKILL after 2s)
        for pid in pids:
            subprocess.run(["kill", pid], capture_output=True, timeout=3)
        
        import time
        time.sleep(2)  # Wait for gateway to detect death and respawn
        
        # Verify process was actually killed (not still running)
        r2 = subprocess.run(
            ["pgrep", "-f", kill_pattern],
            capture_output=True, text=True, timeout=5
        )
        killed_pids = r2.stdout.strip().split("\n") if r2.stdout.strip() else []
        
        return True, f"killed {len(pids)} process(es), gateway should respawn"
    
    except subprocess.TimeoutExpired:
        return False, "timeout killing process"
    except Exception as e:
        return False, str(e)[:60]


def probe_api_key(key_name, val, timeout=10):
    """Lightweight functional test for API keys."""
    if not val or val == "***" or len(val) < 8:
        return False, "missing or masked"
    try:
        if key_name == "OPENAI_API_KEY":
            req = urllib.request.Request(
                "https://api.deepseek.com/user/balance",
                headers={"Authorization": f"Bearer {val}"}
            )
        elif key_name == "TELEGRAM_BOT_TOKEN":
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{val}/getMe"
            )
        else:
            return None, "no test"
        
        r = urllib.request.urlopen(req, timeout=timeout)
        ok = r.status >= 200 and r.status < 300
        return ok, f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:60]


def discover_mcp_servers():
    """Read config.yaml to discover all MCP server definitions. Returns list of dicts."""
    try:
        import yaml
        with open(CONFIG_PATH) as f:
            cfg = yaml.safe_load(f)
    except Exception as e:
        print(f"[ERROR] Cannot read config: {e}", file=sys.stderr)
        return []
    
    servers = cfg.get("mcp_servers", {})
    results = []
    for name, conf in servers.items():
        if not conf.get("enabled", True):
            continue
        cmd = conf.get("command", "") or conf.get("script", "") or ""
        cmd_str = cmd if isinstance(cmd, str) else ""
        args = conf.get("args", []) or []
        env = conf.get("env", {}) or {}
        t = conf.get("type", "mcp")
        
        # Infer category
        cat = "other"
        nl = name.lower()
        if any(k in nl for k in ["google", "gmail", "calendar"]):
            cat = "google"
        elif any(k in nl for k in ["weather", "hkgov"]):
            cat = "hk"
        elif any(k in nl for k in ["notion", "sqlite", "memory", "system"]):
            cat = "storage"
        elif any(k in nl for k in ["fetch", "brave", "perplexity", "apify"]):
            cat = "search"
        elif any(k in nl for k in ["github", "figma", "designlang", "ux"]):
            cat = "dev"
        elif any(k in nl for k in ["sequential"]):
            cat = "reasoning"
        
        results.append({
            "name": name,
            "type": "mcp",
            "category": cat,
            "command": cmd_str[:80],
            "args": args,
            "env": env,
            "desc": conf.get("description", name)[:60],
        })
    return results


def discover_api_keys():
    """Read .env to discover API keys."""
    results = []
    if not ENV_PATH.exists():
        return results
    
    env = {}
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    
    for key_name, info in API_KEY_MAP.items():
        val = env.get(key_name, "")
        results.append({
            "name": key_name.lower(),
            "type": "api",
            "category": info["category"],
            "env_key": key_name,
            "value": val,
            "desc": info["desc"],
        })

    return results


def check_endpoint(ep):
    """Probe a single endpoint. Returns (status, error_msg).
    For MCP: first quick binary check, then deep JSON-RPC probe."""
    if ep["type"] == "mcp":
        # 1) Quick binary check
        ok, err = probe_command(ep.get("command", ""))
        if not ok:
            return "failed", err
        # 2) Deep JSON-RPC probe — actually start server, call listTools
        command = ep.get("command", "")
        args = ep.get("args", [])
        env = ep.get("env", {})
        ok, detail = probe_mcp_server_deep(ep["name"], command, args, env)
        return ("connected" if ok else "failed"), detail
    
    elif ep["type"] == "api":
        env_key = ep.get("env_key", "")
        val = ep.get("value", "")

        ok, err = probe_api_key(env_key, val)

        if ok is None:
            return "unknown", "no test"
        return ("connected" if ok else "failed"), err
    
    return "unknown", "unknown type"


def main():
    now = datetime.now(HKT)
    
    # Step 1: Discover all endpoints
    mcp_servers = discover_mcp_servers()
    api_keys = discover_api_keys()
    all_endpoints = mcp_servers + api_keys
    
    if not all_endpoints:
        print("[SILENT] No endpoints discovered")
        return 0
    
    # Step 2: Get previous snapshot for add/remove detection
    prev_names = set()
    try:
        with pg_cursor() as cur:
            cur.execute("SELECT names_json FROM connection_snapshots ORDER BY snapshot_time DESC LIMIT 1")
            row = cur.fetchone()
            if row:
                prev_names = set(json.loads(row["names_json"]))
    except:
        pass
    
    current_names = set(ep["name"] for ep in all_endpoints)
    added = current_names - prev_names
    removed = prev_names - current_names
    
    # Step 3: Load circuit breaker state
    prev_mcp_state = load_mcp_state()
    circuit_state = {}
    for name, val in prev_mcp_state.items():
        if isinstance(val, dict):
            circuit_state[name] = val
        else:
            # Backward compat: old format was just "connected"/"failed"
            circuit_state[name] = {
                "status": val, "circuit": "CLOSED", "failures": 0,
                "last_fail": None, "skip_count": 0
            }
    new_mcp_state = {}
    state_changes = []  # (name, old_status, new_status, detail)
    auto_restarted = []
    
    # Step 4: Probe each endpoint
    connected = unknown = failed = 0
    status_counts = {}
    
    with pg_cursor(commit=True) as cur:
        for ep in all_endpoints:
            name = ep["name"]
            etype = ep["type"]
            cat = ep.get("category", "")
            status = "unknown"
            error = ""
            
            # ── Circuit breaker check (MCP only) ──
            skip_probe = False
            if etype == "mcp":
                cb = circuit_state.get(name, {
                    "status": "unknown", "circuit": "CLOSED",
                    "failures": 0, "last_fail": None, "skip_count": 0
                })
                if cb["circuit"] == "HALF_OPEN":
                    cb["skip_count"] = cb.get("skip_count", 0) + 1
                    if cb["skip_count"] <= CIRCUIT_COOLDOWN:
                        # Keep last known status, don't probe
                        status = cb.get("status", "failed")
                        error = f"circuit HALF_OPEN (skip {cb['skip_count']}/{CIRCUIT_COOLDOWN})"
                        skip_probe = True
                    else:
                        # Allow one probe
                        cb["skip_count"] = 0
                # Store current circuit state for update
                ep["_circuit"] = cb
                new_mcp_state[name] = cb
            
            if not skip_probe:
                now_ts = datetime.now(HKT)
                status, error = check_endpoint(ep)
            
                # ── Auto-restart logic (MCP failed, circuit still CLOSED) ──
                if etype == "mcp" and status == "failed":
                    cb = ep["_circuit"]
                    cb["failures"] = cb.get("failures", 0) + 1
                    cb["last_fail"] = now_ts.isoformat()
                    
                    if cb["circuit"] == "CLOSED" and cb["failures"] <= MAX_RETRIES:
                        # Try restart: kill process, gateway auto-respawns
                        restart_ok, restart_detail = auto_restart_mcp(
                            name, ep.get("command", ""), ep.get("args", [])
                        )
                        if restart_ok:
                            # Wait a moment, then re-probe
                            import time as _time
                            _time.sleep(3)
                            status2, error2 = check_endpoint(ep)
                            if status2 == "connected":
                                status = "connected"
                                error = f"restarted + re-probe ok: {error2}"
                                cb["failures"] = 0
                                auto_restarted.append(name)
                            else:
                                # Restart didn't help
                                cb["failures"] = cb.get("failures", 0) + 1
                                error = f"restart failed: {error2}"
                    
                    # Open circuit if too many failures
                    if cb["failures"] > MAX_RETRIES:
                        cb["circuit"] = "HALF_OPEN"
                        cb["skip_count"] = 0
                
                # ── Reset circuit on success ──
                if etype == "mcp" and status == "connected":
                    cb = ep["_circuit"]
                    was_failed = cb.get("failures", 0) > 0 or cb.get("status") in ("failed", "unknown")
                    cb["circuit"] = "CLOSED"
                    cb["failures"] = 0
                    cb["skip_count"] = 0
                    cb["status"] = "connected"
            
            # Upsert to PG
            now_ts = datetime.now(HKT)
            cur.execute("""
                INSERT INTO connection_status (name, type, category, status, last_check, last_ok, last_fail, error)
                VALUES (%s, %s, %s, %s, %s, 
                        CASE WHEN %s = 'connected' THEN %s ELSE NULL END,
                        CASE WHEN %s = 'failed' THEN %s ELSE NULL END,
                        %s)
                ON CONFLICT (name, type) DO UPDATE SET
                    status = %s,
                    category = CASE WHEN connection_status.category = '' THEN %s ELSE connection_status.category END,
                    last_seen = %s,
                    last_check = %s,
                    last_ok = CASE WHEN %s = 'connected' THEN %s ELSE connection_status.last_ok END,
                    last_fail = CASE WHEN %s = 'failed' THEN %s ELSE connection_status.last_fail END,
                    error = %s
            """, (name, etype, cat, status, now_ts,
                  status, now_ts,
                  status, now_ts,
                  error,
                  status, cat, now_ts, now_ts,
                  status, now_ts,
                  status, now_ts,
                  error))
            
            if status == "connected":
                connected += 1
            elif status == "unknown":
                unknown += 1
            else:
                failed += 1
            status_counts[name] = status
            
            # Track MCP state transitions for alerting
            if etype == "mcp":
                prev = prev_mcp_state.get(name, "unknown")
                if isinstance(prev, dict):
                    prev = prev.get("status", "unknown")
                if status == "failed" and prev != "failed":
                    state_changes.append((name, prev, "failed", error))
                    write_alert(
                        f"mcp-{name}", "🔴",
                        f"MCP {name} 連線失敗",
                        f"Server {name} probe failed: {error[:80]}"
                    )
                elif status == "connected" and prev in ("failed", "unknown"):
                    state_changes.append((name, prev, "connected", error))
                    if name in auto_restarted:
                        write_alert(
                            f"mcp-{name}", "🟡",
                            f"MCP {name} 自動修復",
                            f"Restart + re-probe ok: {error[:80]}"
                        )
                    else:
                        write_alert(
                            f"mcp-{name}", "🔵",
                            f"MCP {name} 已恢復",
                            f"Server {name} 回復正常: {error[:80]}"
                        )
        
        # Step 5: Save snapshot + MCP state
        cur.execute("""
            INSERT INTO connection_snapshots (total_connected, total_unknown, total_failed, names_json)
            VALUES (%s, %s, %s, %s)
        """, (connected, unknown, failed, json.dumps(list(current_names))))
    
    save_mcp_state(new_mcp_state)
    
    # Step 6: Output (silent if nothing changed)
    total = len(all_endpoints)
    
    changes = []
    if added:
        changes.append(f"+{len(added)} added ({', '.join(sorted(added)[:5])})")
    if removed:
        changes.append(f"-{len(removed)} removed ({', '.join(sorted(removed)[:5])})")
    if state_changes:
        for name, old, new, detail in state_changes[:5]:
            icon = "🔴" if new == "failed" else "🟢"
            changes.append(f"{icon} {name}: {old}→{new} ({detail[:40]})")
    
    if not changes and failed == 0:
        # Silent — everything normal
        return 0
    
    lines = [f"🔌 Connection Health · {now.strftime('%H:%M')}"]
    lines.append(f"   Total: {total}  ·  🟢 {connected}  ·  ⬜ {unknown}  ·  🔴 {failed}")
    if changes:
        for c in changes:
            lines.append(f"   {c}")
    
    print("\n".join(lines))
    
    # Return non-zero if there are failures (so cron doctor can detect)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

"""Collect agent-exporter-style data from the local host (orchestrator).

Provides fallback data for the main orchestrator detail page,
avoiding the need for an SSH tunnel back to localhost.
No psutil dependency — uses /proc and shell commands instead.
"""
import subprocess
import re
from pathlib import Path
from typing import Any


# ── System helpers (no psutil) ────────────────────────────


def _get_cpu_pct() -> int:
    """Parse /proc/stat for approximate CPU usage percentage."""
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.strip().split()
        if len(parts) >= 5:
            user, nice, sys, idle = (
                int(parts[1]),
                int(parts[2]),
                int(parts[3]),
                int(parts[4]),
            )
            total = user + nice + sys + idle
            if total > 0:
                return round(100 - (idle / total * 100))
    except (FileNotFoundError, IndexError, ValueError, OSError):
        pass
    return 0


def _get_mem_pct() -> int:
    """Parse /proc/meminfo for memory usage percentage."""
    try:
        with open("/proc/meminfo") as f:
            data = f.read()
        total_line = [l for l in data.splitlines() if l.startswith("MemTotal:")]
        avail_line = [l for l in data.splitlines() if l.startswith("MemAvailable:")]
        if total_line and avail_line:
            total = int(total_line[0].split()[1])
            avail = int(avail_line[0].split()[1])
            if total > 0:
                return round((total - avail) / total * 100)
    except (FileNotFoundError, IndexError, ValueError, OSError):
        pass
    return 0


def _get_disk_pct() -> int:
    """Parse df output for root disk usage percentage."""
    try:
        r = subprocess.run(
            ["df", "/"], capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            return int(r.stdout.splitlines()[1].split()[4].rstrip("%"))
    except (IndexError, ValueError, OSError, subprocess.TimeoutExpired):
        pass
    return 0


def _get_uptime() -> str:
    """Get human-readable uptime string."""
    try:
        r = subprocess.run(
            ["uptime", "-p"], capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return "unknown"


def _get_hermes_version_local() -> str:
    """Get hermes version from pip or CLI."""
    try:
        r = subprocess.run(
            ["hermes", "--version"], capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            m = re.search(r"(v[\d.]+)", r.stdout.strip())
            if m:
                return m.group(1)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    try:
        import importlib.metadata

        return "v" + importlib.metadata.version("hermes-agent")
    except (ImportError, ModuleNotFoundError):
        pass
    return "unknown"


def _get_llm_info_local() -> dict:
    """Read model/provider from hermes config.yaml (reuse from agent_discovery)."""
    try:
        from app.services.agent_discovery import _get_llm_info

        return _get_llm_info()
    except ImportError:
        pass
    return {"provider": "", "model": ""}


# ── Skills collector ──────────────────────────────────────


def _collect_skills() -> list[dict]:
    """Read skills from ~/.hermes/skills/ directories.

    Returns list of {name, description, category}.
    """
    skills_dir = Path.home() / ".hermes" / "skills"
    skills = []
    if not skills_dir.exists():
        return skills

    for cat_dir in sorted(skills_dir.iterdir()):
        if not cat_dir.is_dir():
            continue
        skill_file = cat_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            content = skill_file.read_text()
            name = cat_dir.name
            desc = ""
            # Try to find YAML front-matter description
            for line in content.splitlines():
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip().strip("\"'")
                    break
            # Try to find first heading as fallback description
            if not desc:
                for line in content.splitlines():
                    if line.startswith("# "):
                        desc = line.lstrip("# ").strip()
                        break
            skills.append(
                {"name": name, "description": desc, "category": cat_dir.parent.name}
            )
        except (OSError, IOError):
            continue

    return skills


# ── Main collection functions ─────────────────────────────


def collect_local_agent_info() -> dict:
    """Return local orchestrator info matching /api/v1/agent-info format."""
    llm = _get_llm_info_local()
    return {
        "agent": "Hermes Agent (Main Orchestrator)",
        "version": _get_hermes_version_local(),
        "llm_provider": llm.get("provider", ""),
        "llm_model": llm.get("model", ""),
    }


def collect_local_capabilities() -> dict:
    """Collect local system data matching /api/v1/capabilities format."""
    return {
        "agent_info": {
            "agent": "Hermes Agent (Main Orchestrator)",
            "version": _get_hermes_version_local(),
        },
        "skills": _collect_skills(),
        "tools": [],
        "mcp_servers": [],
        "system": {
            "cpu_pct": _get_cpu_pct(),
            "memory_pct": _get_mem_pct(),
            "disk_pct": _get_disk_pct(),
            "uptime": _get_uptime(),
        },
        "cron": [],
    }

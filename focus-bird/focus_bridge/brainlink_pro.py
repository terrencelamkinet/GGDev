#!/usr/bin/env python3
"""
BrainLink Pro 腦波讀取器 — Windows 版
=====================================
用 pyserial 直接讀 BrainLink Pro 藍牙 COM port。

用法:
  python brainlink_pro.py --scan              # 掃描 COM port
  python brainlink_pro.py --port COM5         # 連接（普通模式）
  python brainlink_pro.py --port COM5 --json  # JSON 輸出
  python brainlink_pro.py --port COM5 --ws 8765  # WebSocket 模式

需要: BrainLinkParser.pyd + pyserial
"""

import argparse, json, sys, time, inspect, os, threading, queue, asyncio
from datetime import datetime

try:
    import websockets
except ImportError:
    websockets = None

# ── Load BrainLinkParser (only needed for connection) ──
try:
    from BrainLinkParser import BrainLinkParser
    _HAS_PARSER = True
except ImportError:
    _HAS_PARSER = False

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("ERROR: 請安裝 pyserial: pip install pyserial")
    sys.exit(1)


# ── Brain data state ──

class BrainData:
    def __init__(self):
        self.attention = 0
        self.meditation = 0
        self.signal = 200
        self.delta = 0
        self.theta = 0
        self.low_alpha = 0
        self.high_alpha = 0
        self.low_beta = 0
        self.high_beta = 0
        self.low_gamma = 0
        self.high_gamma = 0
        self.battery = -1
        self.focus = 0.0
        self.timestamp = 0.0

    def to_dict(self):
        return {
            "attention": self.attention,
            "meditation": self.meditation,
            "signal": self.signal,
            "delta": self.delta,
            "theta": self.theta,
            "lowAlpha": self.low_alpha,
            "highAlpha": self.high_alpha,
            "lowBeta": self.low_beta,
            "highBeta": self.high_beta,
            "lowGamma": self.low_gamma,
            "highGamma": self.high_gamma,
            "battery": self.battery,
            "focus": self.focus,
            "timestamp": self.timestamp,
        }


RELAY_URL = "wss://brainlink.kinet-poc.com/brainlink"
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brainlink_debug.log")


def log_debug(msg):
    """Write debug message to log file (not console)."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except Exception:
        pass


# ── Auto-detect BrainLinkParser parameters ──

def build_parser(state):
    """Build BrainLinkParser with auto-detected parameter names."""
    # Callbacks
    _eeg_count = [0]
    _ext_count = [0]
    
    def on_eeg(data):
        _eeg_count[0] += 1
        if _eeg_count[0] <= 5:
            sig = int(getattr(data, 'signal', -1))
            att = int(getattr(data, 'attention', -1))
            med = int(getattr(data, 'meditation', -1))
            log_debug(f"EEG #{_eeg_count[0]}: sig={sig} att={att} med={med}")
        state.attention = int(getattr(data, 'attention', 0))
        state.meditation = int(getattr(data, 'meditation', 0))
        sig = int(getattr(data, 'signal', 200))
        state.signal = sig
        state.focus = round(state.attention / 100.0, 2) if sig != 200 else 0.0
        state.timestamp = time.time()

    def on_ext(data):
        _ext_count[0] += 1
        if _ext_count[0] <= 3:
            bat = int(getattr(data, 'battery', -1))
            ver = int(getattr(data, 'version', -1))
            log_debug(f"EXT #{_ext_count[0]}: battery={bat} version={ver}")
        state.delta = int(getattr(data, 'delta', 0) or 0)
        state.theta = int(getattr(data, 'theta', 0) or 0)
        state.low_alpha = int(getattr(data, 'lowAlpha', 0) or 0)
        state.high_alpha = int(getattr(data, 'highAlpha', 0) or 0)
        state.low_beta = int(getattr(data, 'lowBeta', 0) or 0)
        state.high_beta = int(getattr(data, 'highBeta', 0) or 0)
        state.low_gamma = int(getattr(data, 'lowGamma', 0) or 0)
        state.high_gamma = int(getattr(data, 'highGamma', 0) or 0)
        state.battery = int(getattr(data, 'battery', -1) or -1)

    def noop(*args, **kwargs):
        pass

    # Get actual param names from the .pyd
    try:
        sig = inspect.signature(BrainLinkParser.__init__)
        param_names = [p for p in sig.parameters.keys() if p != 'self']
    except Exception:
        param_names = []

    # If no names detected, use fallback
    if not param_names:
        # Try common patterns
        for attempt in [
            {'eeg_callback': on_eeg, 'eeg_extend_callback': on_ext,
             'gyro_callback': noop, 'rr_callback': noop, 'raw_callback': noop},
            {'eeg_callback': on_eeg, 'extend_callback': on_ext,
             'gyro_callback': noop, 'rr_callback': noop, 'raw_callback': noop},
            {'on_eeg': on_eeg, 'on_extend': on_ext,
             'on_gyro': noop, 'on_rr': noop, 'on_raw': noop},
            {'callback_eeg': on_eeg, 'callback_extend': on_ext,
             'callback_gyro': noop, 'callback_rr': noop, 'callback_raw': noop},
        ]:
            try:
                p = BrainLinkParser(**attempt)
                print(f"  ✓ 使用參數: {list(attempt.keys())}")
                return p
            except TypeError:
                continue
        raise RuntimeError("無法匹配 BrainLinkParser 參數名")

    # Map detected names to callbacks
    kwargs = {}
    for name in param_names:
        lower = name.replace('_', '').replace('-', '').lower()
        if any(k in lower for k in ['eegcallback', 'eeg_callback', 'oneeg', 'callbackeeg']):
            kwargs[name] = on_eeg
        elif any(k in lower for k in ['extend', 'ext', 'eeg_extend', 'eeg_ext', 'eeg_extendcallback']):
            kwargs[name] = on_ext
        elif any(k in lower for k in ['gyro']):
            kwargs[name] = noop
        elif any(k in lower for k in ['rr']):
            kwargs[name] = noop
        elif any(k in lower for k in ['raw']):
            kwargs[name] = noop
        else:
            # Unknown parameter - try eeg callback as default
            kwargs[name] = on_eeg

    print(f"  ✓ 自動識別參數: {list(kwargs.keys())}")
    return BrainLinkParser(**kwargs)


# ── Serial reader ──

def read_serial(port, baud=115200, output_json=False, ws_port=None, relay=False):
    if not _HAS_PARSER:
        print("ERROR: BrainLinkParser.pyd 未找到")
        print("請下載: https://github.com/Macrotellect/BrainLinkParser-Python")
        print("然後將 BrainLinkParser.pyd 放喺呢個 folder")
        return

    state = BrainData()

    print(f" 連接 {port} @ {baud} baud...")
    parser = build_parser(state)

    # Try cushy_serial first (official BrainLink library), fallback to pyserial
    using_cushy = False
    _raw_count = [0]
    _last_raw_len = 0
    _parse_errors = [0]
    _last_raw_time = time.time()
    try:
        from cushy_serial import CushySerial
        ser = CushySerial(port, baud)

        @ser.on_message()
        def handle_msg(msg: bytes):
            global _last_raw_time, _parse_errors
            _last_raw_time = time.time()
            _raw_count[0] += 1
            _last_raw_len = len(msg)
            try:
                parser.parse(msg)
            except Exception as e:
                _parse_errors[0] += 1
                if _parse_errors[0] <= 10:
                    log_debug(f"parse error #{_parse_errors[0]}: {e} (len={len(msg)})")

        using_cushy = True
        print(f" ✓ 使用 cushy_serial 連接成功！")
    except Exception as e:
        print(f"  cushy_serial fail: {e}")
        print(f"  轉用 pyserial...")
        ser = serial.Serial(port, baud, timeout=0.1)
        ser.reset_input_buffer()
        time.sleep(0.5)
        ser.reset_input_buffer()
        print(f" ✓ 使用 pyserial 連接成功！")
    print(f"   訊號強度: <50=最佳, 50-150=可用, >150=弱/斷線")
    print(f"   Debug log: {LOG_FILE}")
    if relay:
        print(f"   Relay: {RELAY_URL}")
    print("-" * 50)

    # Optional WebSocket
    clients: set = set()
    if ws_port:
        if websockets is None:
            print("  ⚠ websockets 未安裝，請 pip install websockets")
        else:

            async def ws_h(ws):
                clients.add(ws)
                try:
                    async for _ in ws: pass
                finally:
                    clients.discard(ws)

            async def ws_b():
                while True:
                    if clients:
                        p = json.dumps(state.to_dict())
                        dead = set()
                        for c in clients:
                            try:
                                await c.send(p)
                            except:
                                dead.add(c)
                        clients -= dead
                    await asyncio.sleep(0.1)

            async def ws_start():
                s = await websockets.serve(ws_h, "0.0.0.0", ws_port)
                print(f"  WebSocket: ws://0.0.0.0:{ws_port}")
                await ws_b()

            t = threading.Thread(target=lambda: asyncio.run(ws_start()), daemon=True)
            t.start()

    # Relay mode — connect to remote server
    if relay:
        _relay_q = queue.Queue()
        _relay_connected = [False]

        async def relay_sender():
            try:
                async with websockets.connect(RELAY_URL) as ws:
                    _relay_connected[0] = True
                    log_debug("relay connected")
                    while True:
                        try:
                            data = _relay_q.get(timeout=5)
                            await ws.send(data)
                        except queue.Empty:
                            # Send keepalive
                            try:
                                await ws.send(json.dumps({"ping": 1}))
                            except:
                                break
            except Exception as e:
                log_debug(f"relay: {e}")
                _relay_connected[0] = False

        def relay_worker():
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(relay_sender())

        rt = threading.Thread(target=relay_worker, daemon=True)
        rt.start()
        time.sleep(0.5)

    # Main read loop
    buf = bytearray()
    last_out = 0

    try:
        while True:
            # Read data based on connection type
            if using_cushy:
                # cushy_serial mode — on_message callback handles parsing
                time.sleep(0.1)
            else:
                # pyserial mode — manual reading + parsing
                if ser.in_waiting:
                    chunk = ser.read(ser.in_waiting)
                    buf.extend(chunk)

                    while len(buf) >= 4:
                        if buf[0] != 0xAA or buf[1] != 0xAA:
                            buf.pop(0)
                            continue
                        if len(buf) < 4: break
                        plen = buf[3]
                        total = 4 + plen + 1
                        if len(buf) < total: break
                        pkt = bytes(buf[:total])
                        buf = buf[total:]
                        try:
                            parser.parse(pkt)
                        except:
                            pass

            # Output (both modes)
            now = time.time()
            if now - last_out >= 0.5:
                last_out = now
                s = state.signal
                has_data = s != 200

                # Relay: send to remote server
                if relay:
                    try:
                        _relay_q.put_nowait(json.dumps(state.to_dict()))
                    except:
                        pass

                if output_json:
                    print(json.dumps(state.to_dict()), flush=True)
                else:
                    bar = "█" * max(0, 5 - s // 30) + "░" * min(5, s // 30)
                    # Debug info when no signal
                    try:
                        time_since_raw = now - _last_raw_time
                        raw_info = f" raw:{_raw_count[0]}pkts/{time_since_raw:.0f}s"
                        if _parse_errors[0] > 0:
                            raw_info += f" err:{_parse_errors[0]}"
                    except:
                        raw_info = ""
                    status = "🟢" if has_data else "🔴"
                    print(
                        f"\r{status} 集中:{state.attention:>3} "
                        f"放鬆:{state.meditation:>3} "
                        f"訊號:[{bar}] {s:>3}{raw_info}",
                        end="", flush=True
                    )

    except KeyboardInterrupt:
        print("\n\n已中斷。")
    finally:
        ser.close()


def scan_ports():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("沒有發現 COM port。先藍牙配對 BrainLink Pro。")
        return

    print("可用 COM Port:")
    print("-" * 60)
    for p in sorted(ports, key=lambda x: x.device):
        tag = "🔵 BT" if "bluetooth" in p.description.lower() or "bt" in p.description.lower() else "   "
        print(f"  {tag} {p.device:6s} — {p.description}")
    print("-" * 60)
    print("💡 BrainLink Pro 有兩個 COM port，揀 OUTPUT 嗰個")
    print("   去 藍牙設定 > 更多藍牙選項 > COM 端口 確認")
    print()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="BrainLink Pro EEG Reader")
    ap.add_argument("--port", help="COM port (e.g. COM5)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--scan", action="store_true", help="Scan COM ports")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--ws", type=int, help="WebSocket port")
    ap.add_argument("--relay", action="store_true", help="Relay to remote server")
    args = ap.parse_args()

    if args.scan:
        scan_ports()
        sys.exit(0)

    if not args.port:
        print("用法:")
        print("  python brainlink_pro.py --scan")
        print("  python brainlink_pro.py --port COM5")
        print("  python brainlink_pro.py --port COM5 --json")
        print("  python brainlink_pro.py --port COM5 --ws 8765")
        sys.exit(1)

    read_serial(args.port, args.baud, args.json, args.ws, args.relay)

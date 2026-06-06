#!/usr/bin/env python3
"""
BrainLink Pro → Focus Bird Relay Bridge
BrainLink_Pro sends raw EEG wave (code 0x80).
Parses raw EEG → dynamic baseline → attention score.

Logs:
  brainlink_{ts}_data.log   — per-packet EEG data (CSV format)
  brainlink_{ts}_issue.log  — issues with codes (E001-E010)
"""
import asyncio, json, sys, time, statistics, os, traceback
from collections import deque

try:
    from bleak import BleakScanner, BleakClient
except ImportError:
    print("❌ pip install bleak websockets"); sys.exit(1)

try:
    import websockets
except ImportError:
    print("❌ pip install bleak websockets"); sys.exit(1)

# ===== CONFIG =====
RELAY_URL = "wss://brainlink.kinet-poc.com/brainlink"
BRAINLINK_MAC = "C0:E2:FC:2D:AF:C0"

# ===== Smoothing =====
MEDIAN_WINDOW = 80
BASELINE_WINDOW = 300
SENSITIVITY = 2.0
BLINK_THRESHOLD = 250
LOG_INTERVAL = 10

# ===== Issue Codes =====
# E001: BLE connection fail
# E002: WebSocket connection fail
# E003: No data timeout (>5s without packet)
# E004: Poor signal quality (>150 for 10s+)
# E005: Packet parse error
# E006: Baseline not calibrated yet
# E007: Attention stuck (>30s same side without crossing 50)
# E008: Blink/artifact spike detected
# E009: Rate drop (<5Hz sustained)
# E010: Unknown / catch-all

LOG_PREFIX = f"brainlink_{int(time.time())}"

class IssueLogger:
    def __init__(self):
        self._fp = None
        self._recent_issues = deque(maxlen=20)
        try:
            path = f"{LOG_PREFIX}_issue.log"
            self._fp = open(path, "w", encoding="utf-8")
            self._fp.write(f"=== BrainLink Bridge Issue Log ===\n")
            self._fp.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            self._fp.write(f"Format: TIME | CODE | DESC\n\n")
            self._fp.flush()
            print(f"  📝 Issue log: {os.path.abspath(path)}")
        except Exception as e:
            print(f"  ⚠️ Issue log error: {e}")

    def log(self, code: str, desc: str):
        now = time.strftime("%H:%M:%S")
        line = f"{now} | {code} | {desc}\n"
        if self._fp:
            try:
                self._fp.write(line)
                self._fp.flush()
            except: pass
        self._recent_issues.append((code, desc))
        # Also print to console
        print(f"  🐛 {code}: {desc}")

    def close(self):
        if self._fp:
            try:
                elapsed = "..."
                self._fp.write(f"\n=== End ===\n")
                self._fp.close()
            except: pass
            self._fp = None


class DataLogger:
    def __init__(self):
        self._fp = None
        try:
            path = f"{LOG_PREFIX}_data.log"
            self._fp = open(path, "w", newline="")
            self._fp.write("time,raw_amp,median_amp,baseline,attention,signal\n")
            self._fp.flush()
            print(f"  📊 Data log: {os.path.abspath(path)}")
        except Exception as e:
            print(f"  ⚠️ Data log error: {e}")

    def write(self, line: str):
        if self._fp:
            try:
                self._fp.write(line)
            except: pass

    def flush(self):
        if self._fp:
            try: self._fp.flush()
            except: pass

    def close(self):
        if self._fp:
            try: self._fp.close()
            except: pass
            self._fp = None


class BrainLinkState:
    def __init__(self, issue_log: IssueLogger, data_log: DataLogger):
        self.ilog = issue_log
        self.dlog = data_log
        self.attention = 50
        self.meditation = 50
        self.signal = 200
        self.last_packet = 0.0
        self.raw_window = deque(maxlen=MEDIAN_WINDOW)
        self.clean_window = deque(maxlen=MEDIAN_WINDOW)
        self.baseline_window = deque(maxlen=BASELINE_WINDOW)
        self.packet_count = 0
        self._last_log_time = 0
        self._last_signal_warn = 0
        self._last_att_stuck_check = time.time()
        self._last_att_side = 0  # -1=below50, 0=unknown, 1=above50
        self._packet_ts = deque(maxlen=50)
        self._baseline_ready = False

    def close(self):
        self.dlog.close()
        self.ilog.close()

    def parse(self, data: bytes, ws) -> bool:
        self.last_packet = time.time()
        self._packet_ts.append(self.last_packet)
        pos = 0
        parsed_any = False
        while pos < len(data) - 3:
            if data[pos] != 0xAA or data[pos + 1] != 0xAA:
                pos += 1; continue
            pkt_len = data[pos + 2]
            pkt_end = pos + 3 + pkt_len + 1
            if pkt_end > len(data): break
            payload = data[pos + 3:pos + 3 + pkt_len]
            c1 = (~sum(data[pos + 2:pos + 3 + pkt_len]) & 0xFF)
            c2 = (~sum(payload) & 0xFF)
            if c1 != data[pos + 3 + pkt_len] and c2 != data[pos + 3 + pkt_len]:
                pos += 1; continue
            i = 0
            while i < len(payload):
                code = payload[i]; i += 1
                if code == 0x55: continue
                if i >= len(payload): break
                if code < 0x80:
                    val = payload[i]; i += 1
                    if code == 0x02: self.signal = val
                    elif code == 0x04: self.attention = max(0, min(100, val))
                    elif code == 0x05: self.meditation = max(0, min(100, val))
                else:
                    s_len = payload[i]; i += 1
                    if i + s_len <= len(payload):
                        if code == 0x80 and s_len == 2:
                            raw = (payload[i] << 8) | payload[i + 1]
                            if raw > 32767: raw -= 65536
                            self._process(abs(raw))
                        i += s_len
            pos = pkt_end
            parsed_any = True
            if pos + 1 < len(data) and data[pos] == 0x23 and data[pos + 1] == 0x23:
                pos += 2
        if parsed_any:
            payload = {"attention": self.attention, "meditation": self.meditation,
                       "signal": self.signal, "timestamp": time.time()}
            try: asyncio.create_task(self._send(ws, payload))
            except: pass
        return True

    def _process(self, amplitude: int):
        self.packet_count += 1
        self.raw_window.append(amplitude)
        if amplitude < BLINK_THRESHOLD:
            self.clean_window.append(amplitude)
        else:
            if self.packet_count > 20:
                self.ilog.log("E008", f"Blink spike: amp={amplitude}")
        if len(self.clean_window) < 20:
            return

        median_amp = statistics.median(self.clean_window)
        self.baseline_window.append(median_amp)

        if len(self.baseline_window) < 30:
            if self.packet_count % 100 == 0 and not self._baseline_ready:
                self.ilog.log("E006", f"Calibrating... {len(self.baseline_window)}/30 samples")
            return

        if not self._baseline_ready:
            self._baseline_ready = True
            baseline = statistics.mean(self.baseline_window)
            self.ilog.log("I001", f"Baseline ready: {baseline:.0f}")

        baseline = statistics.mean(self.baseline_window)
        delta = (median_amp - baseline) / max(baseline, 1)
        norm = 0.5 + delta * SENSITIVITY * 0.1
        norm = max(0.0, min(1.0, norm))
        self.attention = max(0, min(100, int(norm * 100)))

        # Signal quality
        now = time.time()
        recent = sum(1 for t in self._packet_ts if now - t < 2.0)
        if recent >= 15:
            self.signal = max(0, self.signal - 3)
        elif recent < 5 and self.packet_count > 50:
            self.signal = min(200, self.signal + 2)
            if self.signal > 150 and now - self._last_signal_warn > 30:
                self._last_signal_warn = now
                self.ilog.log("E009", f"Low rate: {recent}/2s")

        # Check stuck attention (same side for >30s)
        now_side = 1 if self.attention > 50 else (-1 if self.attention < 50 else 0)
        if now_side != self._last_att_side:
            self._last_att_side = now_side
            self._last_att_stuck_check = now
        elif now - self._last_att_stuck_check > 30:
            self._last_att_stuck_check = now
            self.ilog.log("E007", f"Att stuck: side={'>' if now_side>0 else '<' if now_side<0 else '='}50 for 30s+")

        # Data log
        self.dlog.write(f"{now:.1f},{amplitude},{median_amp},{baseline:.0f},{self.attention},{self.signal}\n")

        # Console stats
        if now - self._last_log_time >= LOG_INTERVAL:
            self._last_log_time = now
            self.dlog.flush()
            mn = statistics.mean(self.raw_window)
            mx = max(self.raw_window)
            bl = baseline
            dir_symbol = "⬇" if self.attention > 55 else ("⬆" if self.attention < 45 else "➡")
            print(f"  📊 EEG: raw={mn:3.0f}±{mx-mn:3.0f} med={median_amp:3.0f} base={bl:3.0f} | {dir_symbol} att={self.attention:2d} sig={self.signal:2d}")

    async def _send(self, ws, payload):
        try: await ws.send(json.dumps(payload))
        except websockets.ConnectionClosed: pass


async def find_brainlink():
    if BRAINLINK_MAC: return BRAINLINK_MAC
    print("🔍 Scanning...")
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        if "brainlink" in (d.name or "").lower():
            return d.address
    return None

async def connect_and_run():
    ilog = IssueLogger()
    dlog = DataLogger()
    address = await find_brainlink()
    if not address:
        ilog.log("E001", "BrainLink not found on BLE")
        return
    async for ws in websockets.connect(RELAY_URL, ping_interval=10):
        print(f"✅ Relay connected | BLE to {address}...")
        try:
            async with BleakClient(address, timeout=20) as client:
                print(f"✅ BLE connected")
                state = BrainLinkState(ilog, dlog)
                data_char = None
                for svc in client.services:
                    for char in svc.characteristics:
                        if "notify" in char.properties:
                            if not data_char: data_char = char
                            if "6e400003" in char.uuid.lower(): data_char = char; break
                if not data_char:
                    ilog.log("E001", "No notify characteristic found")
                    return
                print(f"  📡 {data_char.uuid}")
                await client.start_notify(data_char, lambda s, d: state.parse(d, ws))
                print("✅ Listening... (Ctrl+C)")
                last_ok = time.time()
                while True:
                    await asyncio.sleep(3)
                    age = time.time() - state.last_packet
                    now = time.time()
                    if age > 5 and now - last_ok > 15:
                        last_ok = now
                        ilog.log("E003", f"No data for {age:.0f}s")
                    elif state.signal > 150:
                        if now - last_ok > 10:
                            last_ok = now
                            ilog.log("E004", f"Poor signal: sig={state.signal}")
                    else:
                        last_ok = now
                        print(f"  🧠 att={state.attention} sig={state.signal}")
        except asyncio.CancelledError:
            raise
        except Exception as e:
            ilog.log("E010", f"{type(e).__name__}: {str(e)[:100]}")
            await asyncio.sleep(3)
        finally:
            try: state.close()
            except NameError: pass
            except: pass
            try: ilog.close()
            except: pass
            try: dlog.close()
            except: pass

async def main():
    print("=" * 50)
    print("🧠 BrainLink Pro → Focus Bird (dynamic baseline)")
    print("=" * 50)
    while True:
        try:
            await connect_and_run()
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"⚠️ {e}")
            traceback.print_exc()
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())

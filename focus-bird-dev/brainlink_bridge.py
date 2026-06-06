#!/usr/bin/env python3
"""
BrainLink Pro → Focus Bird Relay Bridge
BrainLink_Pro sends raw EEG wave (code 0x80), not processed attention/meditation.
This script parses raw EEG and computes a focus score from signal amplitude.
"""
import asyncio, json, sys, time, statistics
from collections import deque

try:
    from bleak import BleakScanner, BleakClient
except ImportError:
    print("❌ pip install bleak websockets")
    sys.exit(1)

try:
    import websockets
except ImportError:
    print("❌ pip install websockets")
    sys.exit(1)

# ===== CONFIG =====
RELAY_URL = "wss://brainlink.kinet-poc.com/brainlink"
BRAINLINK_MAC = "C0:E2:FC:2D:AF:C0"
NUS_RX_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# ===== Raw EEG → Focus Score =====
# Use rolling median + strong EMA for smooth output.
# Raw EEG amplitude is naturally spiky; median suppresses blink/movement artifacts.
MEDIAN_WINDOW = 80      # ~8 seconds at 10Hz — median suppresses artifacts
EMA_ALPHA = 0.03        # very slow EMA on top of median
AMPLITUDE_MIN = 3
AMPLITUDE_MAX = 200     # wider range to accommodate spikes
BLINK_THRESHOLD = 250   # ignore single samples above this (blinks)
LOG_INTERVAL = 10        # print stats every N seconds

class BrainLinkState:
    def __init__(self):
        self.attention = 50
        self.meditation = 50
        self.signal = 200
        self.last_packet = 0.0
        self.smooth_focus = 0.5      # 0.0-1.0 after median + EMA
        self.raw_window = deque(maxlen=MEDIAN_WINDOW)
        self.clean_window = deque(maxlen=MEDIAN_WINDOW)  # after blink rejection
        self.packet_count = 0
        self._last_log_time = 0
        self._rate_tracker = deque(maxlen=20)

    def parse(self, data: bytes, ws) -> bool:
        """Parse BrainLink_Pro packet stream.
        Format: [0xAA, 0xAA, len, code, sub_len, data..., checksum, 0x23, 0x23]
        Each packet can contain one or more code rows.
        Also handles concatenated multi-packet buffers.
        """
        self.last_packet = time.time()
        self._rate_tracker.append(self.last_packet)
        now = self.last_packet
        if len(self._rate_tracker) >= 5:
            window = now - self._rate_tracker[0]
            self.packet_rate = len(self._rate_tracker) / window if window > 0 else 0

        pos = 0
        parsed_any = False

        while pos < len(data) - 3:
            # Find sync bytes
            if data[pos] != 0xAA or data[pos + 1] != 0xAA:
                pos += 1
                continue

            pkt_len = data[pos + 2]
            pkt_end = pos + 3 + pkt_len + 1  # +1 for checksum

            if pkt_end > len(data):
                break

            # Verify packet
            calc_cs = (~sum(data[pos + 2:pos + 3 + pkt_len]) & 0xFF)
            actual_cs = data[pos + 3 + pkt_len]
            if calc_cs != actual_cs:
                # Try simpler checksum: payload only
                payload = data[pos + 3:pos + 3 + pkt_len]
                alt_cs = (~sum(payload) & 0xFF)
                if alt_cs != actual_cs:
                    pos += 1
                    continue

            # Parse payload rows
            i = 0
            payload = data[pos + 3:pos + 3 + pkt_len]
            while i < len(payload):
                code = payload[i]
                i += 1
                if code == 0x55:  # Extended
                    continue
                if i >= len(payload):
                    break
                if code < 0x80:
                    val = payload[i]
                    i += 1
                    if code == 0x02:  # Signal quality
                        self.signal = val
                        if val > 150:
                            self.attention = 0  # no signal = no focus
                    elif code == 0x04:  # Attention (if device sends it)
                        self.attention = max(0, min(100, val))
                    elif code == 0x05:  # Meditation (if device sends it)
                        self.meditation = max(0, min(100, val))
                else:
                    s_len = payload[i]
                    i += 1
                    if i + s_len <= len(payload):
                        if code == 0x80 and s_len == 2:
                            # Raw EEG: 2 bytes, big-endian, signed
                            raw = (payload[i] << 8) | payload[i + 1]
                            if raw > 32767:
                                raw -= 65536
                            self._process_raw_eeg(abs(raw))
                        i += s_len
            pos = pkt_end
            parsed_any = True

            # Also skip the 0x23 0x23 terminator if present
            if pos + 1 < len(data) and data[pos] == 0x23 and data[pos + 1] == 0x23:
                pos += 2

        if parsed_any:
            # Forward computed data (fire-and-forget send)
            payload = {
                "attention": self.attention,
                "meditation": self.meditation,
                "signal": self.signal,
                "timestamp": time.time(),
            }
            try:
                asyncio.create_task(self._send(ws, payload))
            except Exception:
                pass
        return True

    def _process_raw_eeg(self, amplitude: int):
        """Convert raw EEG amplitude to attention score."""
        self.packet_count += 1
        self.raw_window.append(amplitude)

        # Reject blinks/artifacts (single massive spikes)
        if amplitude < BLINK_THRESHOLD:
            self.clean_window.append(amplitude)

        # Need minimum samples for median
        if len(self.clean_window) < 20:
            return

        # Median of clean window (robust to remaining artifacts)
        median_amp = statistics.median(self.clean_window)

        # Clamp + normalize to 0.0-1.0
        clamped = max(AMPLITUDE_MIN, min(AMPLITUDE_MAX, median_amp))
        norm = (clamped - AMPLITUDE_MIN) / (AMPLITUDE_MAX - AMPLITUDE_MIN)

        # Very slow EMA on top of median
        self.smooth_focus = EMA_ALPHA * norm + (1 - EMA_ALPHA) * self.smooth_focus

        # Map to 0-100
        self.attention = max(0, min(100, int(self.smooth_focus * 100)))

        # Signal quality from packet rate + amplitude stability
        now = time.time()
        rate = len(self._rate_tracker) / max(0.01, now - list(self._rate_tracker)[0]) if len(self._rate_tracker) >= 5 else 0
        if rate > 8 and median_amp < 100:
            self.signal = max(0, self.signal - 2)
        else:
            self.signal = min(200, self.signal + 1)

        # Logging every LOG_INTERVAL seconds
        if now - self._last_log_time >= LOG_INTERVAL:
            self._last_log_time = now
            mn = statistics.mean(self.raw_window)
            mx = max(self.raw_window)
            md = median_amp if len(self.clean_window) > 0 else 0
            # Focus direction indicator
            dir_symbol = "⬇" if self.attention > 55 else ("⬆" if self.attention < 45 else "➡")
            print(f"  📊 EEG raw: min={min(self.raw_window):3d} mean={mn:3.0f} median={md:3d} max={mx:3d} | {dir_symbol} att={self.attention:2d} sig={self.signal:2d}")

    async def _send(self, ws, payload):
        try:
            await ws.send(json.dumps(payload))
        except websockets.ConnectionClosed:
            pass


async def find_brainlink():
    if BRAINLINK_MAC:
        return BRAINLINK_MAC
    print("🔍 Scanning...")
    devices = await BleakScanner.discover(timeout=10)
    for d in devices:
        if "brainlink" in (d.name or "").lower():
            print(f"  ✅ {d.name} @ {d.address}")
            return d.address
    return None


async def connect_and_run():
    address = await find_brainlink()
    if not address:
        print("❌ BrainLink not found. Set BRAINLINK_MAC in script.")
        return

    state = BrainLinkState()

    async for ws in websockets.connect(RELAY_URL, ping_interval=10):
        print(f"✅ Relay connected")
        print(f"🔌 BLE to {address}...")

        try:
            async with BleakClient(address, timeout=20) as client:
                print(f"✅ BLE connected")

                # Find notify characteristic
                data_char = None
                for svc in client.services:
                    for char in svc.characteristics:
                        if "notify" in char.properties:
                            if not data_char:
                                data_char = char
                            if "6e400003" in char.uuid.lower():
                                data_char = char
                                break
                    if "6e400003" in (svc.uuid.lower() if hasattr(svc, 'uuid') else ''):
                        break

                if not data_char:
                    print("❌ No notify char found")
                    return

                print(f"  📡 {data_char.uuid}")

                await client.start_notify(data_char, lambda s, d: state.parse(d, ws))
                print("✅ Listening... (Ctrl+C)")

                while True:
                    await asyncio.sleep(3)
                    age = time.time() - state.last_packet
                    rate = state.packet_rate
                    if age > 3:
                        print(f"  ⏳ No data ({age:.0f}s)")
                    elif state.signal > 150:
                        print(f"  ⚠️ sig={state.signal} rate={rate:.0f}/s")
                    else:
                        print(f"  🧠 att={state.attention} sig={state.signal} rate={rate:.0f}/s")

        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"❌ {e}")
            await asyncio.sleep(3)


async def main():
    print("=" * 50)
    print("🧠 BrainLink Pro → Focus Bird (raw EEG)")
    print("=" * 50)
    while True:
        try:
            await connect_and_run()
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"⚠️ {e}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
focus_bridge_windows.py
BrainLink EEG → WebSocket bridge for Focus Bird Pro
Supports: Windows COM port + BLE
Usage:
  python focus_bridge_windows.py --scan
  python focus_bridge_windows.py --port COM5
  python focus_bridge_windows.py --port COM5 --age 8 --threshold 35
"""

import asyncio, json, time, argparse, sys
from datetime import datetime

# ── Try importing optional packages ──────────────────────────
try:
    import serial, serial.tools.list_ports
    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False
    print("[WARN] pyserial not found. Install: pip install pyserial")

try:
    import websockets
    HAS_WS = True
except ImportError:
    HAS_WS = False
    print("[ERROR] websockets not found. Install: pip install websockets")
    sys.exit(1)

# ── BrainLink MindSet protocol parser ────────────────────────
SYNC1, SYNC2, SYNC3 = 0xAA, 0xAA, 0x04

class MindSetParser:
    """Parse BrainLink/ThinkGear serial stream."""
    def __init__(self):
        self.buf = bytearray()
        self.data = {
            'attention':0,'meditation':0,'signal':200,
            'delta':0,'theta':0,'lowAlpha':0,'highAlpha':0,
            'lowBeta':0,'highBeta':0,'lowGamma':0,'midGamma':0,
        }

    def feed(self, raw: bytes):
        self.buf.extend(raw)
        packets = []
        while len(self.buf) >= 4:
            # Find sync bytes
            if self.buf[0] != 0xAA or self.buf[1] != 0xAA:
                self.buf.pop(0); continue
            plen = self.buf[2]
            if plen == 0xAA:
                self.buf.pop(0); continue
            if len(self.buf) < plen + 4:
                break
            payload = self.buf[3:3+plen]
            chk = (~sum(payload) & 0xFF)
            recv_chk = self.buf[3+plen]
            if chk == recv_chk:
                p = self._parse(payload)
                if p:
                    packets.append(p)
            self.buf = self.buf[4+plen:]
        return packets

    def _parse(self, payload):
        i = 0
        updated = False
        while i < len(payload):
            code = payload[i]; i += 1
            if code == 0x02:   # Signal quality
                self.data['signal'] = payload[i]; i += 1; updated = True
            elif code == 0x04: # Attention
                self.data['attention'] = payload[i]; i += 1; updated = True
            elif code == 0x05: # Meditation
                self.data['meditation'] = payload[i]; i += 1; updated = True
            elif code == 0x80: # Raw wave (2 bytes) — skip
                i += 3
            elif code == 0x83: # EEG power (24 bytes)
                bands = ['delta','theta','lowAlpha','highAlpha',
                         'lowBeta','highBeta','lowGamma','midGamma']
                for b in bands:
                    if i+3 <= len(payload):
                        v = (payload[i]<<16)|(payload[i+1]<<8)|payload[i+2]
                        self.data[b] = v; i += 3
                updated = True
            else:
                break
        return dict(self.data) if updated else None


# ── WebSocket server ──────────────────────────────────────────
clients = set()

async def ws_handler(ws):
    clients.add(ws)
    try:
        async for msg in ws:
            try:
                d = json.loads(msg)
                # Accept threshold/age from game (optional)
                print(f"[WS] recv from game: {d}")
            except Exception:
                pass
    except Exception:
        pass
    finally:
        clients.discard(ws)

async def broadcast(data: dict):
    if not clients:
        return
    msg = json.dumps(data)
    dead = set()
    for c in clients:
        try:
            await c.send(msg)
        except Exception:
            dead.add(c)
    clients -= dead


# ── Serial reader ─────────────────────────────────────────────
async def serial_loop(port, baud, age, threshold):
    if not HAS_SERIAL:
        print("[ERROR] pyserial required for serial mode.")
        return
    parser = MindSetParser()
    try:
        ser = serial.Serial(port, baud, timeout=1)
        print(f"[Serial] Opened {port} @ {baud} baud")
    except Exception as e:
        print(f"[Serial] ERROR: {e}")
        return

    while True:
        try:
            raw = ser.read(64)
            if raw:
                packets = parser.feed(raw)
                for p in packets:
                    p['timestamp'] = int(time.time()*1000)
                    if age:      p['age']       = age
                    if threshold: p['threshold'] = threshold
                    await broadcast(p)
                    ts = datetime.now().strftime('%H:%M:%S')
                    print(f"[{ts}] att={p['attention']:3d} med={p['meditation']:3d} sig={p['signal']:3d}")
        except serial.SerialException as e:
            print(f"[Serial] Disconnected: {e}")
            await asyncio.sleep(3)
            try:
                ser = serial.Serial(port, baud, timeout=1)
                print(f"[Serial] Reconnected to {port}")
            except Exception:
                pass
        await asyncio.sleep(0.005)


# ── Demo loop (no hardware) ───────────────────────────────────
async def demo_loop(age, threshold):
    """Simulate brain signal for testing without hardware."""
    import math, random
    t = 0
    print("[Demo] Running simulated EEG (no hardware). Press Ctrl+C to stop.")
    while True:
        t += 1
        att = int(45 + 35*math.sin(t*0.04) + random.gauss(0,5))
        att = max(0, min(100, att))
        med = int(50 + 20*math.sin(t*0.03+1) + random.gauss(0,4))
        med = max(0, min(100, med))
        data = {
            'attention': att, 'meditation': med, 'signal': 0,
            'theta': 15000+random.randint(-2000,2000),
            'highBeta': 8000+random.randint(-1000,1000),
            'timestamp': int(time.time()*1000),
        }
        if age:       data['age']       = age
        if threshold: data['threshold'] = threshold
        await broadcast(data)
        ts = datetime.now().strftime('%H:%M:%S')
        print(f"[{ts}] [DEMO] att={att:3d} med={med:3d}", end='\r')
        await asyncio.sleep(1.0)


# ── Main ──────────────────────────────────────────────────────
async def main(args):
    server = await websockets.serve(ws_handler, 'localhost', args.ws_port)
    print(f"[WS] Server listening on ws://localhost:{args.ws_port}")
    print("[WS] Waiting for Focus Bird Pro browser connection...")

    if args.scan:
        if HAS_SERIAL:
            ports = list(serial.tools.list_ports.comports())
            print("\nAvailable COM ports:")
            for p in ports:
                print(f"  {p.device} — {p.description}")
            if not ports:
                print("  (none found)")
        else:
            print("pyserial not installed.")
        return

    if args.port:
        await serial_loop(args.port, args.baud, args.age, args.threshold)
    else:
        await demo_loop(args.age, args.threshold)

    await server.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Focus Bird Pro — BrainLink Bridge')
    parser.add_argument('--port',      type=str,  default=None,  help='COM port (e.g. COM5)')
    parser.add_argument('--baud',      type=int,  default=57600, help='Baud rate (default 57600)')
    parser.add_argument('--ws-port',   type=int,  default=8765,  help='WebSocket port (default 8765)')
    parser.add_argument('--age',       type=int,  default=None,  help='Age to send to game')
    parser.add_argument('--threshold', type=int,  default=None,  help='Focus threshold override')
    parser.add_argument('--scan',      action='store_true',      help='List COM ports and exit')
    args = parser.parse_args()
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\n[Bridge] Stopped.")

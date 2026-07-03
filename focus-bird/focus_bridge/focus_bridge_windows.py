import argparse
import asyncio
import json
import sys
import time
from dataclasses import dataclass, asdict

try:
    from cushy_serial import CushySerial
except ImportError:
    print('Install cushy-serial: pip install cushy-serial')
    sys.exit(1)

try:
    from BrainLinkParser import BrainLinkParser
except ImportError:
    print('Download BrainLinkParser from Macrotellect and place it beside this file or in Python path.')
    sys.exit(1)

@dataclass
class BrainState:
    attention: int = 0
    meditation: int = 0
    signal: int = 200
    delta: int = 0
    theta: int = 0
    lowAlpha: int = 0
    highAlpha: int = 0
    lowBeta: int = 0
    highBeta: int = 0
    lowGamma: int = 0
    highGamma: int = 0
    focusLevel: float = 0.0
    shouldDive: bool = False
    threshold: int = 42
    age: int = 6
    timestamp: float = 0.0

class FocusBridge:
    def __init__(self, port: str, baud: int, ws_port: int, age: int, threshold: int, alpha: float):
        self.port = port
        self.baud = baud
        self.ws_port = ws_port
        self.age = age
        self.threshold = threshold
        self.alpha = alpha
        self.serial = None
        self.parser = None
        self.clients = set()
        self.state = BrainState(age=age, threshold=threshold)
        self.running = True

    def on_eeg(self, data):
        self.state.attention = int(getattr(data, 'attention', 0) or 0)
        self.state.meditation = int(getattr(data, 'meditation', 0) or 0)
        self.state.signal = int(getattr(data, 'signal', 200) or 200)
        self.state.focusLevel = round((1 - self.alpha) * self.state.focusLevel + self.alpha * self.state.attention, 2)
        self.state.shouldDive = self.state.focusLevel >= self.threshold and self.state.signal < 80
        self.state.timestamp = time.time()

    def on_extend_eeg(self, data):
        for k in ['delta','theta','lowAlpha','highAlpha','lowBeta','highBeta','lowGamma','highGamma']:
            setattr(self.state, k, int(getattr(data, k, 0) or 0))

    def on_gyro(self, x, y, z):
        return

    def on_rr(self, rr1, rr2, rr3):
        return

    def on_raw(self, raw):
        return

    def start_serial(self):
        self.parser = BrainLinkParser(
            eeg_callback=self.on_eeg,
            eeg_extend_callback=self.on_extend_eeg,
            gyro_callback=self.on_gyro,
            rr_callback=self.on_rr,
            raw_callback=self.on_raw,
        )
        self.serial = CushySerial(self.port, self.baud)

        @self.serial.on_message()
        def handle_message(msg: bytes):
            self.parser.parse(msg)

        print(f'Connected to BrainLink on {self.port} @ {self.baud}')

    async def handle_client(self, websocket):
        self.clients.add(websocket)
        await websocket.send(json.dumps(asdict(self.state)))
        try:
            async for message in websocket:
                try:
                    cmd = json.loads(message)
                    if 'threshold' in cmd:
                        self.threshold = int(cmd['threshold'])
                        self.state.threshold = self.threshold
                    if 'age' in cmd:
                        self.age = int(cmd['age'])
                        self.state.age = self.age
                except Exception:
                    pass
        finally:
            self.clients.discard(websocket)

    async def broadcast(self):
        while self.running:
            if self.clients:
                payload = json.dumps(asdict(self.state))
                dead = []
                for ws in list(self.clients):
                    try:
                        await ws.send(payload)
                    except Exception:
                        dead.append(ws)
                for ws in dead:
                    self.clients.discard(ws)
            await asyncio.sleep(0.1)

    async def run(self):
        import websockets
        self.start_serial()
        server = await websockets.serve(self.handle_client, '0.0.0.0', self.ws_port)
        print(f'WebSocket server ready: ws://localhost:{self.ws_port}')
        print('Open the HTML game and connect to the local websocket URL.')
        try:
            await self.broadcast()
        finally:
            server.close()
            await server.wait_closed()

def scan_ports():
    try:
        import serial.tools.list_ports
    except ImportError:
        print('Install pyserial: pip install pyserial')
        return
    ports = serial.tools.list_ports.comports()
    if not ports:
        print('No COM ports found.')
        return
    for p in ports:
        print(f'{p.device} - {p.description}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BrainLink Windows bridge for Focus Bird Pro')
    parser.add_argument('--port', help='Windows COM port, for example COM5')
    parser.add_argument('--baud', type=int, default=115200)
    parser.add_argument('--ws-port', type=int, default=8765)
    parser.add_argument('--age', type=int, default=6)
    parser.add_argument('--threshold', type=int, default=42)
    parser.add_argument('--alpha', type=float, default=0.18, help='EMA smoothing factor for attention to focusLevel')
    parser.add_argument('--scan', action='store_true')
    args = parser.parse_args()

    if args.scan:
        scan_ports()
        sys.exit(0)
    if not args.port:
        print('Missing COM port. Example: python focus_bridge_windows.py --port COM5')
        sys.exit(1)
    asyncio.run(FocusBridge(args.port, args.baud, args.ws_port, args.age, args.threshold, args.alpha).run())

#!/usr/bin/env python3
"""
BrainLink → WebSocket Bridge
將 BrainLink 腦波裝置嘅 attention 數值傳去 browser game.html

用法：
  1. pip install cushy-serial websockets
  2. 藍牙連接 BrainLink（電腦會見到 COM port / /dev/cu.BrainLink_Pro）
  3. 搵 output COM port（見 FAQ）
  4. python brainlink_bridge.py --port /dev/cu.BrainLink_Pro

game.html 會自動用 externalMode 連接 ws://localhost:8765
"""

import argparse
import asyncio
import websockets
import json
import sys
import signal

# Try importing SDK
try:
    from cushy_serial import CushySerial
except ImportError:
    print("❌ 請先安裝 cushy-serial: pip install cushy-serial")
    sys.exit(1)

try:
    from BrainLinkParser import BrainLinkParser
except ImportError:
    print("❌ 請先下載 BrainLinkParser.pyd / .so")
    print("   下載: https://github.com/Macrotellect/BrainLinkParser-Python")
    print("   放入同一個 folder 或者 Python path")
    sys.exit(1)


class BrainLinkBridge:
    def __init__(self, port, baud=115200, threshold=40):
        self.port = port
        self.baud = baud
        self.threshold = threshold  # attention 大過呢個值 = 下沉
        self.current_attention = 0
        self.serial = None
        self.parser = None
        self.websocket_clients = set()
        self.server = None

    def on_eeg(self, data):
        """BrainLink EEG callback — 收到 attention 數值"""
        self.current_attention = data.attention
        # 可以 print 睇 debug
        # print(f"attention={data.attention}", end="\r")

    def on_extend_eeg(self, data):
        pass  # 唔需要用

    def on_gyro(self, x, y, z):
        pass  # 唔需要用

    def on_rr(self, rr1, rr2, rr3):
        pass  # 唔需要用

    def on_raw(self, raw):
        pass  # 唔需要用

    def start_serial(self):
        """連接 BrainLink 藍牙 serial"""
        try:
            self.parser = BrainLinkParser(
                eeg_callback=self.on_eeg,
                eeg_extend_callback=self.on_extend_eeg,
                gyro_callback=self.on_gyro,
                rr_callback=self.on_rr,
                raw_callback=self.on_raw
            )
            self.serial = CushySerial(self.port, self.baud)

            @self.serial.on_message()
            def handle_message(msg: bytes):
                self.parser.parse(msg)

            print(f"✅ BrainLink 已連接: {self.port} @ {self.baud}")
            return True
        except Exception as e:
            print(f"❌ 連接失敗: {e}")
            return False

    async def broadcast(self):
        """每秒 broadcast 一次 attention 去所有 websocket clients"""
        while True:
            if self.websocket_clients:
                # 判斷 should_dive (attention > threshold)
                should_dive = self.current_attention > self.threshold
                payload = json.dumps({
                    "attention": self.current_attention,
                    "shouldDive": should_dive,
                    "threshold": self.threshold
                })
                # 廣播俾所有 connected browsers
                dead = set()
                for ws in self.websocket_clients:
                    try:
                        await ws.send(payload)
                    except:
                        dead.add(ws)
                self.websocket_clients -= dead
            await asyncio.sleep(0.1)  # 10Hz update

    async def handle_websocket(self, websocket):
        """新 browser 連接 WebSocket"""
        self.websocket_clients.add(websocket)
        print(f"🖥️  Browser connected ({len(self.websocket_clients)} total)")
        try:
            async for _ in websocket:
                pass  # 唔使收 message
        finally:
            self.websocket_clients.discard(websocket)
            print(f"🖥️  Browser disconnected ({len(self.websocket_clients)} total)")

    async def start_websocket_server(self, host="0.0.0.0", port=8765):
        """起 WebSocket server"""
        self.server = await websockets.serve(
            self.handle_websocket, host, port
        )
        print(f"🌐 WebSocket 伺服器: ws://{host}:{port}")
        print(f"   注意：同機玩就用 ws://localhost:{port}")
        print(f"   LAN玩就用你部機嘅IP: ws://YOUR_IP:{port}")

    async def run(self):
        """主程式"""
        if not self.start_serial():
            return

        await self.start_websocket_server()

        # 同時 broadcast + 等 server
        await asyncio.gather(
            self.broadcast(),
            self.server.wait_closed()
        )


def find_available_ports():
    """自動偵測可用 COM port (唔係BrainLink都用)"""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("🔍 冇發現任何 COM port / serial device")
        print("   請確認藍牙已配對 BrainLink")
        return
    print("\n🔍 可用嘅 COM port:")
    for p in ports:
        print(f"   {p.device}  —  {p.description}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BrainLink → WebSocket Bridge")
    parser.add_argument("--port", help="COM port (例如 COM3 / /dev/cu.BrainLink_Pro)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--threshold", type=int, default=40, help="Attention threshold for dive (default: 40)")
    parser.add_argument("--ws-port", type=int, default=8765, help="WebSocket port (default: 8765)")
    parser.add_argument("--scan", action="store_true", help="Scan available COM ports")
    args = parser.parse_args()

    if args.scan:
        find_available_ports()
        sys.exit(0)

    if not args.port:
        print("❌ 請指定 COM port，例如:")
        print("   Windows: python brainlink_bridge.py --port COM3")
        print("   Mac:     python brainlink_bridge.py --port /dev/cu.BrainLink_Pro")
        print("   Linux:   python brainlink_bridge.py --port /dev/ttyUSB0")
        print("")
        print("   or:  python brainlink_bridge.py --scan  (掃描可用 port)")
        sys.exit(1)

    bridge = BrainLinkBridge(args.port, args.baud, args.threshold)
    try:
        asyncio.run(bridge.run())
    except KeyboardInterrupt:
        print("\n👋 Bridge 已關閉")

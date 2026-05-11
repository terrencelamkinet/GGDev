#!/usr/bin/env python3
"""
BrainLink 模擬器 — 唔使硬體，用 keyboard 模擬腦波
等你可以試 bridge + game.html 連接係咪 work

用法:
  python brainlink_simulator.py
  
然後 browser 開:
  https://ggdev-bzr58.ondigitalocean.app/focus_bird/game.html?ws=ws://localhost:8765

控制:
  按 ↑ 專注力上升（飛鳥下沉食金幣）
  按 ↓ 專注力下降（飛鳥上浮）
  q 或 Ctrl+C 離開
"""

import asyncio
import websockets
import json
import time
import sys

# Windows keyboard input — use msvcrt
import msvcrt
import threading

class Simulator:
    def __init__(self, ws_host="0.0.0.0", ws_port=8765, threshold=40):
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.threshold = threshold
        self.attention = 50  # 起始 50
        self.clients = set()
        self.running = True

    def key_listener(self):
        """背景 thread 監聽 keyboard"""
        print("🎮 控制：")
        print("   ↑ 專注力上升（飛鳥下沉）")
        print("   ↓ 專注力下降（飛鳥上浮）")
        print("   r 重置到 50")
        print("   q 離開")
        print("")
        print(f"  當前 threshold: {self.threshold}")
        print(f"  attention > {self.threshold} → spacePressed = true (下沉)")
        print("")

        while self.running:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # arrow keys
                    key = msvcrt.getch()
                    if key == b'H':  # ↑
                        self.attention = min(100, self.attention + 10)
                        print(f"⬆ 專注力 +10 → {self.attention}  {'⏬ 下沉' if self.attention > self.threshold else '⬆ 上浮'}")
                    elif key == b'P':  # ↓
                        self.attention = max(0, self.attention - 10)
                        print(f"⬇ 專注力 -10 → {self.attention}  {'⏬ 下沉' if self.attention > self.threshold else '⬆ 上浮'}")
                elif key == b'r' or key == b'R':
                    self.attention = 50
                    print(f"🔄 重置到 50  {'⏬ 下沉' if self.attention > self.threshold else '⬆ 上浮'}")
                elif key == b'q' or key == b'Q':
                    print("👋 關閉中...")
                    self.running = False

    async def broadcast(self):
        """每秒10次 broadcast 俾 browser"""
        while self.running:
            if self.clients:
                payload = json.dumps({
                    "attention": self.attention,
                    "shouldDive": self.attention > self.threshold,
                    "threshold": self.threshold
                })
                dead = set()
                for ws in self.clients:
                    try:
                        await ws.send(payload)
                    except:
                        dead.add(ws)
                self.clients -= dead
            await asyncio.sleep(0.1)

    async def handle_client(self, websocket):
        self.clients.add(websocket)
        print(f"\n🖥️  Browser 已連接！({len(self.clients)} total)")
        print(f"   試吓按 ↑↓ 睇飛鳥反應\n")
        try:
            async for _ in websocket:
                pass
        finally:
            self.clients.discard(websocket)
            print(f"🖥️  Browser 斷線 ({len(self.clients)} 剩餘)")

    async def start(self):
        print("")
        print("=" * 50)
        print("🧠 BrainLink 模擬器")
        print("=" * 50)
        print("")

        # Start key listener in background
        thread = threading.Thread(target=self.key_listener, daemon=True)
        thread.start()

        # Start WebSocket server
        server = await websockets.serve(
            self.handle_client, self.ws_host, self.ws_port
        )
        
        print(f"🌐 WebSocket server: ws://{self.ws_host}:{self.ws_port}")
        print("")
        print("📱 用 browser 開呢個 URL：")
        print(f"   https://ggdev-bzr58.ondigitalocean.app/focus_bird/game.html?ws=ws://localhost:{self.ws_port}")
        print("")
        print("⚠️  如果瀏覽器話 WebSocket 連接失敗：")
        print("   1. 檢查 firewall 有冇 block port 8765")
        print("   2. 試用 ws://127.0.0.1:8765 代替 ws://localhost:8765")
        print("")
        
        await asyncio.gather(
            self.broadcast(),
            server.wait_closed()
        )


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="BrainLink Simulator for Windows")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket port")
    parser.add_argument("--threshold", type=int, default=40, help="Attention threshold")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address")
    args = parser.parse_args()

    sim = Simulator(args.host, args.port, args.threshold)
    try:
        asyncio.run(sim.start())
    except KeyboardInterrupt:
        print("\n👋 已關閉")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        print("")
        print("🔧 如果係 'No module named ...'，試試：")
        print("   pip install websockets")

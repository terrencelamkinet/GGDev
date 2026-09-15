#!/usr/bin/env python3
"""
BrainLink 模擬器 v2 — 模擬真實腦波模式 + wss:// 支援
等你可以試 Agent Relay Server + game.html 連接係咪 work

用法:
  # 連去 Agent Relay Server
  python brainlink_simulator.py --url ws://localhost:8765/brainlink

  # 本機 mode (舊式 direct to browser)
  python brainlink_simulator.py --local

  # 用 config
  python brainlink_simulator.py --config config.txt

控制:
  ↑ 專注力上升（attention +15）
  ↓ 專注力下降（attention -15）
  r 重置到隨機 baseline (40-60)
  q 離開
"""

import asyncio
import json
import math
import random
import sys
import os
import time

# Windows keyboard input — use msvcrt
import msvcrt
import threading


class Simulator:
    def __init__(
        self,
        ws_host="0.0.0.0",
        ws_port=8765,
        threshold=65,
        url=None,
        use_local=False,
    ):
        self.ws_host = ws_host
        self.ws_port = ws_port
        self.threshold = threshold
        self.url = url
        self.use_local = use_local

        # 真實模擬參數
        self.attention = 50.0  # float 可以 graduel 變化
        self.baseline = 50.0  # baseline（隨時間 slow drift）
        self.target = 50.0  # target attention（慢慢趨向）
        self.signal = 200  # signal quality (200=no signal, 0=good)
        self.meditation = random.randint(30, 60)

        # 波動參數
        self.drift_speed = 0.5  # baseline drift speed
        self.noise_amplitude = 2.0  # noise amplitude
        self.signal_quality = 200  # 初始冇訊號，3秒後變好

        self.clients = set()
        self.running = True
        self.agent_ws = None
        self.frame = 0

    def key_listener(self):
        """背景 thread 監聽 keyboard"""
        print("🎮 控制：")
        print("   ↑ 專注力上升（+15）")
        print("   ↓ 專注力下降（-15）")
        print("   r 重置 baseline")
        print("   q 離開")
        print("")
        print(f"  當前 threshold: {self.threshold}")

        while self.running:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b"\xe0":  # arrow keys
                    key = msvcrt.getch()
                    if key == b"H":  # ↑
                        self.attention = min(100, self.attention + 15)
                        self.target = self.attention
                        print(
                            f"⬆ +15 → {self.attention:.0f}  "
                            f"{'⏬ 下沉' if self.attention > self.threshold else '⬆ 上浮'}"
                        )
                    elif key == b"P":  # ↓
                        self.attention = max(0, self.attention - 15)
                        self.target = self.attention
                        print(
                            f"⬇ -15 → {self.attention:.0f}  "
                            f"{'⏬ 下沉' if self.attention > self.threshold else '⬆ 上浮'}"
                        )
                elif key == b"r" or key == b"R":
                    self.baseline = random.uniform(40, 60)
                    self.target = self.baseline
                    print(f"🔄 重置 baseline → {self.baseline:.0f}")
                elif key == b"q" or key == b"Q":
                    print("👋 關閉中...")
                    self.running = False

    def update_attention(self):
        """更新 attention 用 realistic 模式（gradual rise/fall, noise）"""
        self.frame += 1

        # 訊號質量：3秒後變好
        if self.frame < 30:  # 3 seconds at 10Hz
            self.signal = 200  # no signal yet
        else:
            self.signal = random.randint(0, 30)  # good signal

        # Baseline slow drift (random walk)
        if random.random() < 0.02:  # 2% chance per tick
            self.baseline += random.uniform(-5, 5)
            self.baseline = max(20, min(80, self.baseline))

        # Target 慢慢趨向 baseline
        self.target += (self.baseline - self.target) * 0.01

        # Gradual approach to target
        diff = self.target - self.attention
        step = diff * 0.08  # 8% 趨向 target per tick

        # Add noise (sinusoidal + random)
        noise = math.sin(self.frame * 0.05) * 1.5 + random.gauss(0, 1.5)
        noise = max(-3, min(3, noise))

        self.attention += step + noise
        self.attention = max(0, min(100, self.attention))

    def get_brain_data(self):
        """返回 brain data dict（同真 bridge 一樣格式）"""
        return {
            "attention": round(self.attention),
            "meditation": self.meditation,
            "signal": self.signal,
            "shouldDive": self.attention > self.threshold,
            "delta": 0,
            "theta": 0,
            "lowAlpha": 0,
            "highAlpha": 0,
            "lowBeta": 0,
            "highBeta": 0,
            "lowGamma": 0,
            "highGamma": 0,
        }

    async def connect_to_agent(self):
        """連接到 Agent Relay Server"""
        import websockets

        print(f"🔄 連接 Agent Server: {self.url}")
        try:
            self.agent_ws = await websockets.connect(self.url)
            print(f"✅ 已連接 Agent Server ({self.url})")
            return True
        except Exception as e:
            print(f"❌ 連接失敗: {e}")
            return False

    async def send_to_agent(self):
        """每秒10次 send brain data 去 Agent Server"""
        print("\n🧠 開始模擬真實腦波（gradual changes + noise）")
        print("   按 ↑↓ 手動控制，或等佢自動 drift\n")

        while self.running:
            self.update_attention()

            if self.agent_ws:
                try:
                    payload = json.dumps(self.get_brain_data())
                    await self.agent_ws.send(payload)
                    # Show status every 10 frames
                    if self.frame % 10 == 0:
                        status = (
                            "🔴" if self.signal > 150 else "🟢"
                        )
                        print(
                            f"  {status} attention={self.attention:.0f} "
                            f"signal={self.signal}   "
                            f"{'⏬' if self.attention > self.threshold else '⬆'}",
                            end="\r",
                        )
                except Exception as e:
                    print(f"\n⚠️  Send error: {e}")
                    self.agent_ws = None
                    print("🔄 嘗試重新連接...")
                    await asyncio.sleep(3)
                    await self.connect_to_agent()
            else:
                # No connection — try reconnect
                await asyncio.sleep(2)

            await asyncio.sleep(0.1)

    # ===== Local mode (old) =====
    async def broadcast_local(self):
        """每秒10次 broadcast 俾 browser (local mode)"""
        while self.running:
            self.update_attention()
            if self.clients:
                payload = json.dumps(self.get_brain_data())
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
        print(f"   按 ↑↓ 睇飛鳥反應\n")
        try:
            async for _ in websocket:
                pass
        finally:
            self.clients.discard(websocket)
            print(f"🖥️  Browser 斷線 ({len(self.clients)} 剩餘)")

    async def start_local(self):
        """舊式 local mode"""
        import websockets

        print("\n" + "=" * 50)
        print("🧠 BrainLink 模擬器 v2 (Local Mode)")
        print("=" * 50)

        thread = threading.Thread(target=self.key_listener, daemon=True)
        thread.start()

        server = await websockets.serve(
            self.handle_client, self.ws_host, self.ws_port
        )

        print(f"\n🌐 WebSocket server: ws://{self.ws_host}:{self.ws_port}")
        print("📱 Browser URL:")
        print(
            f"   https://ggdev-bzr58.ondigitalocean.app/focus-bird-dev/focus_bird/game.html?ws=ws://localhost:{self.ws_port}/game"
        )

        await asyncio.gather(self.broadcast_local(), server.wait_closed())

    async def start_agent(self):
        """New agent relay mode"""
        print("\n" + "=" * 50)
        print("🧠 BrainLink 模擬器 v2 (Agent Relay Mode)")
        print("=" * 50)

        thread = threading.Thread(target=self.key_listener, daemon=True)
        thread.start()

        if not await self.connect_to_agent():
            print("⚠️  無法連接 Agent Server，3秒後重試...")
            # Will retry in send_to_agent loop

        await self.send_to_agent()

    async def start(self):
        """Main entry — decide local vs agent"""
        if self.use_local or not self.url:
            await self.start_local()
        else:
            await self.start_agent()


def load_config(config_path):
    """讀取 config.txt 設定檔"""
    config = {}
    if not os.path.exists(config_path):
        return config
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BrainLink Simulator v2 — realistic EEG + wss")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket port (default: 8765)")
    parser.add_argument("--threshold", type=int, default=65, help="Attention threshold (default=65)")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)")
    parser.add_argument("--url", help="Agent Relay URL (例如 ws://localhost:8765/brainlink)")
    parser.add_argument("--config", default="config.txt", help="Config file path")
    parser.add_argument("--local", action="store_true", help="Local mode (no Agent Server)")
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    url = args.url or config.get("AGENT_WS_URL") or config.get("WS_URL")

    sim = Simulator(
        ws_host=args.host,
        ws_port=args.port,
        threshold=args.threshold,
        url=url,
        use_local=args.local or not url,
    )

    try:
        asyncio.run(sim.start())
    except KeyboardInterrupt:
        print("\n👋 已關閉")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        print("\n🔧 試試：pip install websockets")
        sys.exit(1)

#!/usr/bin/env python3
"""
BrainLink → Agent Relay Bridge (for Lenovo X1 Windows)
讀取 BrainLink 腦波資料，經 wss:// 傳去 Agent Relay Server

用法：
  # 用 config.txt
  python brainlink_bridge.py --config config.txt

  # 直接指定
  python brainlink_bridge.py --port COM5 --url wss://agent-server:8765/brainlink

  # 掃描 COM port
  python brainlink_bridge.py --scan

  # 本機模式（唔經 Agent Server，直接 broadcast 俾本地 browser）
  python brainlink_bridge.py --port COM5 --local
"""

import argparse
import asyncio
import json
import os
import sys
import signal
import time

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
        self.threshold = threshold  # attention 大過呢個值 = 下沉 (local mode)
        self.current_attention = 0
        self.current_meditation = 0
        self.current_signal = 200  # 200 = no signal
        self.serial = None
        self.parser = None
        self.websocket_clients = set()  # For local mode
        self.server = None
        self.agent_ws = None  # For agent relay mode
        self.agent_url = None
        self.running = True

    def on_eeg(self, data):
        """BrainLink EEG callback — 收到 attention 數值"""
        self.current_attention = data.attention
        self.current_meditation = data.meditation
        self.current_signal = data.signal

    def on_extend_eeg(self, data):
        pass  # 唔需要用

    def on_gyro(self, x, y, z):
        pass  # 唔需要用

    def on_rr(self, rr1, rr2, rr3):
        pass  # 唔需要用

    def on_raw(self, raw):
        pass  # 唔需要用

    def get_brain_data(self):
        """返回完整 brain data dict"""
        return {
            "attention": self.current_attention,
            "meditation": self.current_meditation,
            "signal": self.current_signal,
            "shouldDive": self.current_attention > self.threshold,
            "delta": 0,
            "theta": 0,
            "lowAlpha": 0,
            "highAlpha": 0,
            "lowBeta": 0,
            "highBeta": 0,
            "lowGamma": 0,
            "highGamma": 0,
        }

    def start_serial(self):
        """連接 BrainLink 藍牙 serial"""
        try:
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

            print(f"✅ BrainLink 已連接: {self.port} @ {self.baud}")
            return True
        except Exception as e:
            print(f"❌ 連接失敗: {e}")
            if "Access is denied" in str(e) or "Permission" in str(e):
                print("   🔧 可能原因：選咗 Incoming COM port（應選 Outgoing port）")
                print("     或在其他程式已開啟此 COM port")
            return False

    async def connect_to_agent(self):
        """連接到 Agent Relay Server 嘅 /brainlink path"""
        import websockets

        print(f"🔄 正在連接 Agent Server: {self.agent_url}")
        try:
            self.agent_ws = await websockets.connect(self.agent_url)
            print(f"✅ 已連接 Agent Server: {self.agent_url}")
            return True
        except Exception as e:
            print(f"❌ 連接 Agent Server 失敗: {e}")
            print("   請確認 Agent Server 已啟動同 firewall 已開 port")
            return False

    async def send_to_agent(self):
        """每秒 10 次 send brain data 去 Agent Server"""
        while self.running:
            if self.agent_ws:
                try:
                    payload = json.dumps(self.get_brain_data())
                    await self.agent_ws.send(payload)
                except Exception as e:
                    print(f"⚠️  Send error: {e}")
                    # Try reconnect
                    self.agent_ws = None
                    print("🔄 嘗試重新連接 Agent Server...")
                    await asyncio.sleep(3)
                    await self.connect_to_agent()
            await asyncio.sleep(0.1)  # 10Hz

    async def broadcast_local(self):
        """每秒 broadcast 一次 attention 去所有 websocket clients (local mode)"""
        while self.running:
            if self.websocket_clients:
                payload = json.dumps(self.get_brain_data())
                dead = set()
                for ws in self.websocket_clients:
                    try:
                        await ws.send(payload)
                    except:
                        dead.add(ws)
                self.websocket_clients -= dead
            await asyncio.sleep(0.1)

    async def handle_websocket(self, websocket):
        """新 browser 連接 WebSocket (local mode)"""
        self.websocket_clients.add(websocket)
        print(f"🖥️  Browser connected ({len(self.websocket_clients)} total)")
        try:
            async for _ in websocket:
                pass
        finally:
            self.websocket_clients.discard(websocket)
            print(f"🖥️  Browser disconnected ({len(self.websocket_clients)} total)")

    async def start_websocket_server(self, host="0.0.0.0", port=8765):
        """起 WebSocket server (local mode)"""
        import websockets

        self.server = await websockets.serve(
            self.handle_websocket, host, port
        )
        print(f"🌐 WebSocket 伺服器: ws://{host}:{port}")
        print(f"   注意：同機玩就用 ws://localhost:{port}")

    async def run_local(self):
        """Local mode — 直接 broadcast 俾 browser"""
        if not self.start_serial():
            return
        await self.start_websocket_server()
        await asyncio.gather(self.broadcast_local(), self.server.wait_closed())

    async def run_agent(self):
        """Agent mode — 經 Agent Server relay"""
        if not self.start_serial():
            return
        if not await self.connect_to_agent():
            print("⚠️  Agent mode 無法連接，請檢查 URL 和 Server 狀態")
            # Keep trying in background
            asyncio.create_task(self._keep_trying_to_connect())

        await self.send_to_agent()

    async def _keep_trying_to_connect(self):
        """Background retry connecting to agent"""
        while self.running and not self.agent_ws:
            await asyncio.sleep(5)
            if not self.agent_ws:
                await self.connect_to_agent()


def find_available_ports():
    """自動偵測可用 COM port (唔係BrainLink都用)"""
    try:
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        if not ports:
            print("🔍 冇發現任何 COM port / serial device")
            print("   請確認藍牙已配對 BrainLink")
            return
        print("\n🔍 可用嘅 COM port:")
        for p in ports:
            label = ""
            if "bluetooth" in p.description.lower() or "bt" in p.description.lower():
                label = " ← Bluetooth!"
            if "outgoing" in p.description.lower():
                label += " ← Outgoing (用呢個!)"
            if "incoming" in p.description.lower():
                label += " ← Incoming (唔好用)"
            print(f"   {p.device}  —  {p.description}{label}")
        print("\n💡 提示：如果藍牙配對咗 BrainLink，應該見到兩組 COM port")
        print("   請揀 Outgoing 嗰個（唔係 Incoming）")
    except ImportError:
        print("🔍 無法掃描 (pyserial 未安裝)")
        print("   安裝: pip install pyserial")


def load_config(config_path):
    """讀取 config.txt 設定檔"""
    config = {}
    if not os.path.exists(config_path):
        print(f"❌ Config 檔案唔存在: {config_path}")
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
    parser = argparse.ArgumentParser(
        description="BrainLink → Agent Relay Bridge (for Windows X1)"
    )
    parser.add_argument("--port", help="COM port (例如 COM3)")
    parser.add_argument("--url", help="Agent WebSocket URL (例如 wss://server:8765/brainlink)")
    parser.add_argument(
        "--config", default="config.txt", help="Config file path (default: config.txt)"
    )
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--threshold", type=int, default=40, help="Attention threshold (default: 40)")
    parser.add_argument("--ws-port", type=int, default=8765, help="WebSocket port for local mode (default: 8765)")
    parser.add_argument("--scan", action="store_true", help="Scan available COM ports")
    parser.add_argument("--local", action="store_true", help="Local mode (no Agent Server)")
    args = parser.parse_args()

    if args.scan:
        find_available_ports()
        sys.exit(0)

    # Load config from file
    config = load_config(args.config)

    # Priority: CLI args > config file
    port = args.port or config.get("BLUETOOTH_COM") or config.get("COM_PORT")
    url = args.url or config.get("AGENT_WS_URL") or config.get("WS_URL")

    if not port:
        print("❌ 請指定 COM port，例如:")
        print("   python brainlink_bridge.py --port COM5")
        print("   or 編輯 config.txt 設定 BLUETOOTH_COM")
        print("")
        print("   or: python brainlink_bridge.py --scan  (掃描可用 port)")
        sys.exit(1)

    # Determine mode
    is_local = args.local or (not url)

    bridge = BrainLinkBridge(port, args.baud, args.threshold)

    try:
        if is_local:
            print("🔌 Local mode (direct to browser)")
            print(f"   用 ws://localhost:{args.ws_port} 連接")
            asyncio.run(bridge.run_local())
        else:
            print(f"🔗 Agent relay mode (X1 → Agent Server → Browser)")
            print(f"   URL: {url}")
            bridge.agent_url = url
            asyncio.run(bridge.run_agent())
    except KeyboardInterrupt:
        print("\n👋 Bridge 已關閉")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        sys.exit(1)

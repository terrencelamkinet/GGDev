#!/usr/bin/env python3
"""
BrainLink Agent Relay Server
Agent Server 上運行，接收 brainlink_bridge.py 嘅 raw data，
做 EMA smoothing + agentNote mapping，然後 relay 去 game.html。

Architecture:
  BrainLink Pro → X1 (brainlink_bridge.py) → wss:// → /brainlink → agent_relay_server.py → /game → browser

Usage:
  python agent_relay_server.py [--port 8765] [--host 0.0.0.0]

websockets v10 & v11+ 兼容
"""

import asyncio
import json
import time
import os
import sys

try:
    import websockets
    from websockets.server import serve
except ImportError:
    print("❌ 請先安裝 websockets: pip install websockets")
    sys.exit(1)


# ===== EMA Smoothing =====
EMA_ALPHA = 0.25  # α=0.25 — 可以調整 (0.1=更穩, 0.5=更快反應)


class BrainRelayState:
    """共享狀態 — 保持最新 brain data 俾所有 /game 連線"""

    def __init__(self):
        self.smooth_attention = 50.0  # EMA smoothed attention
        self.raw_attention = 0
        self.meditation = 0
        self.signal = 200  # 200 = 無訊號
        self.should_dive = False
        self.last_update = 0
        self.game_clients = set()
        self.brainlink_connected = False

    @property
    def agent_note(self):
        """將 signal + attention map 做 agentNote"""
        if self.signal > 150:
            return "no_signal"
        if self.smooth_attention < 50:
            return "low_focus"
        if self.smooth_attention >= 70:
            return "high_focus"
        return "normal"

    def apply_ema(self, raw_attention):
        """指數移動平均"""
        if raw_attention is not None:
            self.raw_attention = raw_attention
            self.smooth_attention = (
                EMA_ALPHA * raw_attention + (1 - EMA_ALPHA) * self.smooth_attention
            )
        self.last_update = time.time()

    def get_game_payload(self):
        """返回俾 game.html 嘅 JSON payload"""
        return {
            "attention": round(self.smooth_attention),
            "meditation": self.meditation,
            "signal": self.signal,
            "shouldDive": self.smooth_attention > 50,  # > 50 下沉
            "focusLevel": round(self.smooth_attention),
            "agentNote": self.agent_note,
        }

    def get_debug_payload(self):
        """完整 debug payload"""
        p = self.get_game_payload()
        p["raw_attention"] = self.raw_attention
        p["smooth_attention"] = round(self.smooth_attention, 2)
        p["brainlink_connected"] = self.brainlink_connected
        p["last_update"] = self.last_update
        return p


# 全域共享狀態
relay_state = BrainRelayState()

# Save path for debug JSON
DEBUG_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brainlink_latest.json")


def save_debug_json(payload):
    """Save latest brain data to local JSON file for debugging"""
    try:
        with open(DEBUG_JSON_PATH, "w") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass  # Best effort


async def handle_brainlink(websocket):
    """
    /brainlink — 接收 brainlink_bridge.py 嘅 raw data
    """
    # Detect path for compat (websockets v10 vs v11+)
    try:
        path = websocket.request.path
    except AttributeError:
        path = websocket.path

    print(f"🔗 BrainLink bridge 已連接 (path: {path})")
    relay_state.brainlink_connected = True

    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                # Extract attention
                raw_attention = data.get("attention")
                if raw_attention is not None:
                    relay_state.apply_ema(raw_attention)

                # Update other fields
                relay_state.meditation = data.get("meditation", relay_state.meditation)
                relay_state.signal = data.get("signal", relay_state.signal)

                # Debug log
                note = relay_state.agent_note
                print(
                    f"🧠 raw={relay_state.raw_attention} "
                    f"smooth={relay_state.smooth_attention:.1f} "
                    f"signal={relay_state.signal} "
                    f"note={note}",
                    end="\r",
                )

                # Broadcast to all /game clients
                if relay_state.game_clients:
                    payload = relay_state.get_game_payload()
                    payload_str = json.dumps(payload)
                    dead = set()
                    for ws in relay_state.game_clients:
                        try:
                            await ws.send(payload_str)
                        except Exception:
                            dead.add(ws)
                    relay_state.game_clients -= dead

                # Save debug JSON
                save_debug_json(relay_state.get_debug_payload())

            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON from bridge: {message[:100]}")
            except Exception as e:
                print(f"⚠️  Error processing brainlink data: {e}")

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        relay_state.brainlink_connected = False
        print("\n🔌 BrainLink bridge 已斷線")


async def handle_game(websocket):
    """
    /game — 傳送處理過嘅 data 俾 browser game.html
    """
    # Detect path for compat
    try:
        path = websocket.request.path
    except AttributeError:
        path = websocket.path

    print(f"🖥️  Game browser 已連接 (path: {path})")
    relay_state.game_clients.add(websocket)

    try:
        # Send current state immediately on connect
        current = relay_state.get_game_payload()
        await websocket.send(json.dumps(current))

        async for _ in websocket:
            pass  # 唔使收 message，只係 send
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        relay_state.game_clients.discard(websocket)
        print(f"🖥️  Game browser 斷線 ({len(relay_state.game_clients)} 剩餘)")


async def main(host="0.0.0.0", port=8765):
    """Start WebSocket server with two paths"""
    print("=" * 50)
    print("🧠 BrainLink Agent Relay Server")
    print("=" * 50)
    print(f"  EMA alpha: {EMA_ALPHA}")
    print(f"  Debug JSON: {DEBUG_JSON_PATH}")
    print()

    async def handler(websocket):
        """Route to correct handler based on path"""
        # websockets v11+ uses websocket.request.path
        # websockets v10 uses websocket.path
        try:
            path = websocket.request.path
        except AttributeError:
            path = websocket.path

        if path == "/brainlink" or path.endswith("/brainlink"):
            await handle_brainlink(websocket)
        elif path == "/game" or path.endswith("/game"):
            await handle_game(websocket)
        else:
            print(f"⚠️  未知路徑: {path}")
            await websocket.close(1000, "Unknown path")

    async with serve(handler, host, port):
        print(f"🌐 Agent Relay Server 已啟動:")
        print(f"     ws://{host}:{port}/brainlink  ← BrainLink Bridge")
        print(f"     ws://{host}:{port}/game       ← Focus Bird Game")
        print(f"     (加上 wss:// 如果經 Cloudflare Tunnel)")
        print()
        print("⏳ 等待 BrainLink bridge 連接...")
        print()

        await asyncio.Future()  # 永遠運行


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="BrainLink Agent Relay Server — relay + EMA smoothing"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Bind address (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8765, help="WebSocket port (default: 8765)"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=EMA_ALPHA,
        help=f"EMA smoothing alpha (default: {EMA_ALPHA})",
    )
    args = parser.parse_args()

    if args.alpha != EMA_ALPHA:
        globals()["EMA_ALPHA"] = args.alpha

    try:
        asyncio.run(main(args.host, args.port))
    except KeyboardInterrupt:
        print("\n👋 Relay Server 已關閉")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        sys.exit(1)

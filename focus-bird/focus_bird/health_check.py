"""Focus Bird — Device health checker for start_focus_bird.bat
Connects to relay, waits for one message with valid brain data.
Exit code: 0 = device ready, 1 = timeout/no device.
"""
import sys
import json
import asyncio
import websockets

RELAY_URL = "wss://brainlink.kinet-poc.com/game"
TIMEOUT = 60  # seconds total

async def main():
    try:
        async with websockets.connect(RELAY_URL, ping_interval=10) as ws:
            deadline = asyncio.get_event_loop().time() + TIMEOUT
            while asyncio.get_event_loop().time() < deadline:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=1)
                    data = json.loads(msg)
                    sig = data.get("signal", 200)
                    att = data.get("attention")
                    # Relay sends: attention, meditation, signal, shouldDive, focusLevel, agentNote
                    # Real brain data: signal < 150 AND attention is a valid number
                    att_ok = isinstance(att, (int, float)) and att >= 0
                    sig_ok = isinstance(sig, (int, float)) and sig >= 0 and sig < 150
                    if att_ok and sig_ok:
                        print("DEVICE_READY")
                        sys.exit(0)
                    else:
                        print(f"Waiting... sig={sig} att={att}", file=sys.stderr)
                except asyncio.TimeoutError:
                    continue
        print("TIMEOUT — No device detected", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR — {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    asyncio.run(main())

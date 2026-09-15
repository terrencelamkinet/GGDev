# Focus Bird v2.0 — Project Context

> 最後更新：2026-05-30 08:15 HKT
> 由 GG Fighter (Hermes Main) @ Terrence 對話建立
> 獨立文件，無需 chat history 即可理解

---

## 1. 專案定位

Focus Bird 係一款**專注力訓練遊戲**（Brain-Computer Interface game），用 BrainLink Pro 腦波儀控制一隻鳥上下移動，收集金幣。目標係訓練持續注意力（sustained attention），透過腦波專注度控制遊戲角色。

## 2. Architecture（完整拓撲）

```
X1 (Windows / brainlink_bridge.py)
  │  BrainLink Pro → serial/BLE
  │  bridge 將 raw data → WebSocket JSON
  │
  ├── wss://brainlink.kinet-poc.com/brainlink
  │     │
  │     ▼
  │   Cloudflare Tunnel (focusbird, permanent)
  │   ┌─────────────────────────────────────┐
  │   │  tunnel ID: 251ee728-d271-4b96-92e6-│
  │   │             6dbd731d8388             │
  │   │  CNAME: brainlink.kinet-poc.com      │
  │   └──────────┬──────────────────────────┘
  │              │
  │              ▼
  │   GG-Fighter VM (Linux, 0.0.0.0:8765)
  │   ┌─────────────────────────────────────┐
  │   │  brainlink_relay.py                 │
  │   │  └── /brainlink → 接收 X1 bridge    │
  │   │  └── /game → 推送俾 browser         │
  │   │  └── EMA smoothing (α=0.25)         │
  │   │  └── agentNote mapping              │
  │   └─────────────────────────────────────┘
  │              │
  │              ▼
  │   Browser (Focus Bird game.html)
  │   ┌─────────────────────────────────────┐
  │   │  Canvas game, teal-blue-green 色盤  │
  │   │  三層 parallax                      │
  │   │  ws://.../game 接收 focus data     │
  │   │  專注高→鳥下沉，專注低→鳥上升      │
  │   └─────────────────────────────────────┘
  │
  └── (瀏覽器直接開 game URL)
      https://ggdev-bzr58.ondigitalocean.app/focus-bird-dev/focus_bird/game.html
      ?ws=wss://brainlink.kinet-poc.com/game
```

### Data Flow (每幀)

1. BrainLink Pro 讀取腦波 raw data（attention/meditation/signal）
2. X1 bridge.py 打包 JSON → wss://.../brainlink
3. relay.py EMA 平滑（α=0.25）→ agentNote mapping
4. relay.py broadcast → 所有 /game WebSocket clients
5. game.html 根據 attention 值控制鳥位置（>50 下沉，<50 上升）

## 3. 部署細節

### Game 檔案（DO App）

| 項目 | URL |
|------|-----|
| v2.0 (dev) | `https://ggdev-bzr58.ondigitalocean.app/focus-bird-dev/focus_bird/game.html` |
| v1.0 (prod) | `https://ggdev-bzr58.ondigitalocean.app/focus-bird/focus_bird/game.html` |
| v1.0 未改動 | v2.0 係獨立目錄，v1.0 保持原樣 |

### Relay Server

- Script: `~/.hermes/scripts/brainlink_relay.py`
- Port: **8765** (bind 0.0.0.0)
- Systemd: `brainlink-relay.service` — 開機自啟
- Log: `/var/log/brainlink-relay.log`
- Debug JSON: `~/.hermes/scripts/brainlink_latest.json`

### Cloudflare Tunnel

- Name: `focusbird`
- ID: `251ee728-d271-4b96-92e6-6dbd731d8388`
- Domain: `brainlink.kinet-poc.com` → tunnel → localhost:8765
- Systemd: `cloudflared-focusbird.service` — 開機自啟
- Credentials: `~/.cloudflared/251ee728-d271-4b96-92e6-6dbd731d8388.json`
- Cert: `~/.cloudflared/cert.pem` (282 bytes)
- Log: `/var/log/cloudflared-focusbird.log`

## 4. Colors / Design (Scientific Palette)

基於兩項認知科學研究（PMC8774152, PMC11410860）：

| 色系 | 佔比 | 色碼 | 用途 |
|------|------|------|------|
| 🟢 青綠 | 55% | #1a6b5a / #2EC4B6 / #A8DADC | 背景、主角鳥、按鈕 |
| 🔵 藍色 | 25% | #1a3a5c / #4361EE / #74B3CE | 夜空、專注光環、Focus Bar 高專注 |
| 🟡 琥珀 | ≤10% | #E8933A / #FFCB77 | 金幣、獎勵特效（<3秒） |
| ⚪ 中性 | 10% | #F4F9F9 / #264653 | 卡片背景、文字 |

- Focus Bar 三階段：橙(低專注) → 青(中) → 藍(高)
- 主角鳥：#2EC4B6 主體 + #F4A261 嘴喙
- 三層 parallax：sky 靜止 / hills 0.15x / ground 1x

## 5. 現有 Systemd Services（GG-Fighter VM）

| Service | Status | Port | Auto-start |
|---------|--------|------|------------|
| `brainlink-relay.service` | ✅ Active | 8765 | ✅ Enabled |
| `cloudflared-focusbird.service` | ✅ Active | tunnel | ✅ Enabled |

## 6. 使用流程

1. **玩家**：開 browser 去 game URL（加 `?ws=wss://.../game`）
2. **BrainLink**：X1 行 `brainlink_bridge.py` → connect wss://brainlink.kinet-poc.com/brainlink
3. **專注**：專注度高 → 鳥下沉（避開障礙物）
4. **放鬆**：專注度低 → 鳥上升
5. **金幣**：收集金幣加分

## 7. 已知限制 / TODO

- 未做 BrainLink EEG 濾波優化（目前只有 EMA）
- game.html 需更新 BrainLink logo 為正確版本（目前用 placeholder）
- relay.py 只有單線程 asyncio，需注意連接數限制
- v1.0 focus-bird/ 目錄未清理 legacy code
- game URL 暫用 DO app，可考慮自訂域名

## 8. 關鍵路徑 / 檔案位置

```
~/.hermes/scripts/brainlink_relay.py    ← relay server
~/.hermes/scripts/brainlink_latest.json ← debug data
~/.cloudflared/                         ← tunnel config + cert
/etc/systemd/system/brainlink-relay.service
/etc/systemd/system/cloudflared-focusbird.service
/home/airoot/projects/ggdev-repo/focus-bird-dev/    ← v2.0 game
/home/airoot/projects/ggdev-repo/focus-bird/        ← v1.0 game
```

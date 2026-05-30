# BrainLink × Focus Bird Integration Guide
### For AI Agent — Lenovo X1 Windows Setup

> **反思修正版 v2** — 修正了三項原版問題：  
> 1. Python 版本必須 3.11（BrainLinkParser.pyd 版本鎖定）  
> 2. 瀏覽器 HTTPS 頁面強制要求 wss:// (非 ws://)  
> 3. websockets v11+ API 變更（handler signature）  

---

## 架構總覽

```
BrainLink Pro (Bluetooth)
    │ Bluetooth SPP → Windows COM (Output port)
    ▼
brainlink_bridge.py  [Lenovo X1, Python 3.11]
    │ wss://AGENT_SERVER:8765/brainlink  (Internet)
    ▼
agent_relay_server.py  [AI Agent Server, public IP]
    │ ai_process() → EMA smoothing + agentNote
    │ wss://AGENT_SERVER:8765/game
    ▼
Focus Bird game.html  [Browser on Lenovo X1]
    ?ws=wss://AGENT_SERVER:8765/game
```

---

## ⚠️ 重要注意事項（原版未提及）

### 1. Python 版本鎖定為 3.11
`BrainLinkParser.pyd` 是預編譯的 C extension，只相容 **Python 3.11.x**。  
其他版本（3.10、3.12、3.13）均會出現 `ImportError`。

確認方式：
```cmd
python --version
# 必須顯示 Python 3.11.x
```

### 2. Windows Bluetooth 會生成兩個 COM Port
BrainLink 配對後，Windows 設備管理員會出現**兩個** Bluetooth COM port：
- **Incoming (COM x)** — 勿用
- **Outgoing (COM y)** — 使用這個

查找方式：
```
設備管理員 → 連接埠 (COM 和 LPT) → 
找 "BrainLink" 或 "Standard Serial over Bluetooth link"
選帶有 "Outgoing" 字樣的
```

### 3. 瀏覽器強制要求 wss://
Focus Bird 部署在 HTTPS（DigitalOcean），瀏覽器安全策略  
**不允許** HTTPS 頁面連接 `ws://`（非加密）。  
Agent Server 必須提供 `wss://`（TLS）。

最簡單方案：使用 Cloudflare Tunnel（免費，零設定）：
```bash
# 在 Agent Server 執行：
cloudflared tunnel --url ws://localhost:8765
# 自動產生 wss://xxxx.trycloudflare.com
```

### 4. websockets 版本相容性
`agent_relay_server.py` 已處理 v10 和 v11+ 兩種 API：
```python
try:
    path = ws.request.path   # websockets v11+
except AttributeError:
    path = ws.path           # websockets v10 fallback
```

---

## 檔案清單

| 檔案 | 運行位置 | 說明 |
|------|---------|------|
| `brainlink_bridge.py` | Lenovo X1 | 讀取 BrainLink，推送到 Agent Server |
| `agent_relay_server.py` | AI Agent Server | WebSocket Relay + AI 邏輯 |
| `setup_once.bat` | Lenovo X1 | 一次性安裝（首次運行）|
| `start_bridge.bat` | Lenovo X1 | 每次啟動 Bridge（讀取 config.txt）|
| `config.txt` | Lenovo X1 | 設定 COM port 和 Agent URL |

---

## Lenovo X1 設定步驟（一次性）

### Step 1 — 配對 BrainLink 藍牙
```
Windows Settings → Bluetooth & Devices → Add Device
→ 選 BrainLink Pro → 配對
配對後：設備管理員 → 連接埠 → 記下 Outgoing COM port (如 COM5)
```

### Step 2 — 下載 BrainLinkParser.pyd
```
https://github.com/Macrotellect/BrainLinkParser-Python
→ Windows 資料夾 → 下載 BrainLinkParser.pyd (Python 3.11 版本)
→ 放到本資料夾（與 brainlink_bridge.py 同一目錄）
```

### Step 3 — 運行 setup_once.bat
雙擊 `setup_once.bat`，它會自動：
- 確認 Python 3.11
- 安裝 `cushy-serial`, `websockets`, `pyserial`
- 掃描並列出 Bluetooth COM ports
- 建立 `config.txt`

### Step 4 — 編輯 config.txt
```ini
BLUETOOTH_COM=COM5        # 改為你的 Outgoing COM port
AGENT_WS_URL=wss://your-agent-server.com:8765/brainlink
```

### Step 5 — 每次使用：雙擊 start_bridge.bat
腳本會自動讀取 `config.txt`、更新 Python 腳本設定、然後啟動 Bridge。

---

## Agent Server 設定步驟

### 安裝
```bash
pip install websockets
```

### 啟動（測試用）
```bash
python agent_relay_server.py
# 輸出：Listening on ws://0.0.0.0:8765
```

### 公開給瀏覽器（wss:// 必須）

**方案 A：Cloudflare Tunnel（最簡單，推薦）**
```bash
# 安裝 cloudflared（一次性）
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/

cloudflared tunnel --url ws://localhost:8765
# 輸出範例：wss://random-name.trycloudflare.com
```

**方案 B：Nginx reverse proxy + Let's Encrypt**
```nginx
server {
    listen 443 ssl;
    server_name your-agent-server.com;
    ssl_certificate     /etc/letsencrypt/live/your-agent-server.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-agent-server.com/privkey.pem;

    location / {
        proxy_pass         http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade    $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host       $host;
    }
}
```

---

## 開啟遊戲

```
https://ggdev-bzr58.ondigitalocean.app/focus-bird/focus_bird/game.html?ws=wss://YOUR_AGENT_SERVER/game
```

> 瀏覽器 console 應顯示：`BrainLink via Agent connected`

---

## JSON 資料格式

### X1 → Agent (`/brainlink`)
```json
{
  "attention":   65,
  "meditation":  40,
  "signal":      200,
  "shouldDive":  false,
  "delta": 0, "theta": 0,
  "lowAlpha": 0, "highAlpha": 0,
  "lowBeta": 0, "highBeta": 0,
  "lowGamma": 0, "highGamma": 0
}
```

### Agent → Game (`/game`)
```json
{
  "attention":   62,
  "meditation":  38,
  "signal":      200,
  "shouldDive":  false,
  "focusLevel":  62,
  "agentNote":   "normal"
}
```

`agentNote` 值：
- `"no_signal"` — 裝置訊號差（signal > 150）
- `"low_focus"` — attention < 50
- `"normal"` — attention 50–69
- `"high_focus"` — attention ≥ 70

---

## AI 平滑邏輯（EMA）

Agent Server 使用指數移動平均（EMA, α=0.25）消除抖動：

```
smooth = 0.25 × raw + 0.75 × previous_smooth
```

效果：單次異常數值只影響 25%，避免鳥因 1–2 個 outlier 急速上下。  
可在 `agent_relay_server.py` 調整 `EMA_ALPHA`（0.1=更穩，0.5=更快反應）。

---

## 故障排查

| 問題 | 原因 | 解決 |
|------|------|------|
| `ImportError: BrainLinkParser` | .pyd 未放在同目錄 / Python 版本不是 3.11 | 確認 Python 3.11 + .pyd 同目錄 |
| `Cannot open COM5` | 選了 Incoming port / 裝置未配對 | 選 Outgoing COM port |
| 遊戲 console 出現 Mixed Content | 用了 ws:// 而非 wss:// | 用 Cloudflare Tunnel 取得 wss:// |
| attention 一直顯示 0 | signal > 150（訊號差） | 戴好裝置，等 signal 降到 < 50 |
| websockets handler error | 版本不相容 | `pip install "websockets>=11"` |


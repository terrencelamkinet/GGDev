# GG 三台 VM 完整還原指南（Full Restore Guide）

> **適用場景**: 新 VM 建立 / 災難還原 / 系統遷移
> **備份位置**: Google Drive → `GG_Backup/YYYY-MM-DD/`
> **備份格式**: `{vm-name}_{type}_{timestamp}.tar.gz`
> **最後更新**: 2026-05-30

---

## 目錄

1. [前置準備](#1-前置準備)
2. [Ubuntu 系統安裝](#2-ubuntu-系統安裝)
3. [基礎工具安裝](#3-基礎工具安裝)
4. [Hermes Agent 安裝（GG Fighter）](#4-hermes-agent-安裝gg-fighter)
5. [OpenClaw 安裝（GG-Work / GG-Person）](#5-openclaw-安裝gg-work--gg-person)
6. [從 Google Drive 還原 AI 數據](#6-從-google-drive-還原-ai-數據)
7. [各 VM 專屬配置](#7-各-vm-專屬配置)
8. [還原驗證清單](#8-還原驗證清單)

---

## 1. 前置準備

### 所需資料
| 項目 | 位置 | 備註 |
|------|------|------|
| Google Drive 備份 | `GG_Backup/` 目錄 | 揀最近一次 full backup |
| Google Drive Token | ~/.hermes/drive_token.json | OAuth token |
| GitHub 個人存取 Token | 你自己嘅 GitHub | 用嚟 push/pull GGDev repo |
| Notion API Key | ~/.config/notion/api_key | 必要 |
| Telegram Bot Token | ~/.hermes/.env | 必要 |

### VM 網絡資訊
| VM | Hostname | 內網 IP | SSH Host |
|----|----------|---------|----------|
| GG Fighter | vmagc-00 | 172.6.15.183 | — (local) |
| GG-Work | gg-work | 172.6.15.181 | gg-work |
| GG-Person | gg-person | 172.6.15.182 | gg-person |

---

## 2. Ubuntu 系統安裝

### 2.1 安裝 Ubuntu 24.04 LTS
```bash
# 下載 Ubuntu 24.04 LTS Server ISO
# https://ubuntu.com/download/server

# 安裝時設定：
# - Hostname: vmagc-00 / gg-work / gg-person
# - Username: airoot
# - SSH: 勾選 Install OpenSSH server
# - 分區: 預設即可（建議最少 50GB root partition）
```

### 2.2 基本系統設定
```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 設定 hostname（視乎邊部 VM）
sudo hostnamectl set-hostname gg-work   # or gg-person / vmagc-00

# 設定時區
sudo timedatectl set-timezone Asia/Hong_Kong

# 設定 SSH key（從現有 VM copy 或 generate new）
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

# 設定 authorized_keys（三台 VM 互通）
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys

# 設定 sudo NOPASSWD
echo 'airoot ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/airoot-nopasswd

# 收緊 SSH 配置
sudo tee -a /etc/ssh/sshd_config << 'EOF'
PasswordAuthentication no
PermitRootLogin prohibit-password
EOF
sudo systemctl restart ssh

# 啟用防火牆
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow from 172.6.15.0/24 to any port 22
sudo ufw --force enable
```

---

## 3. 基礎工具安裝

### 三台 VM 都需要安裝

```bash
# Git
sudo apt install -y git

# Python 3 + pip
sudo apt install -y python3 python3-pip python3-venv

# Node.js (via nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 22
nvm use 22

# 其他工具
sudo apt install -y curl wget tar gzip unzip htop net-tools
```

---

## 4. Hermes Agent 安裝（GG Fighter only）

```bash
# 安裝 Hermes Agent
pip install hermes-agent

# 初始化
hermes setup

# 配置 config
hermes config set provider deepseek
hermes config set model deepseek-v4-flash

# 啟用 MCP
hermes tools enable memory
hermes tools enable sqlite
```

---

## 5. OpenClaw 安裝（GG-Work / GG-Person only）

```bash
# 安裝 OpenClaw Gateway
pip install openclaw-gateway  # 或從 source 安裝

# 初始化 gateway
mkdir -p ~/.openclaw
# 複製 config 或從 backup 還原
```

---

## 6. 從 Google Drive 還原 AI 數據

### 6.1 設置 Google Drive Access

你嘅 drive token 已備份喺 full backup 入面。如果冇 token，需要重新授權：

```bash
# 安裝 rclone 或使用 Python 腳本
# 備份腳本自帶 Drive API，使用時需要 OAuth token
```

### 6.2 下載 backup

手動從 Google Drive 下載：
1. 去 https://drive.google.com/drive/folders/18gCCi4O7z9FAcyCKvZvCVxKgY4OxTLyi
2. 進入 `GG_Backup/`
3. 揀最近一次 full backup 日期 folder
4. 下載以下三個檔案：
   - `gg-fighter_full_YYYYMMDD_HHMM.tar.gz`
   - `gg-work_full_YYYYMMDD_HHMM.tar.gz`
   - `gg-person_full_YYYYMMDD_HHMM.tar.gz`

### 6.3 還原 GG Fighter

```bash
# 解壓還原
tar xzf gg-fighter_full_YYYYMMDD_HHMM.tar.gz -C /tmp/restore

# 還原 .hermes/
cp -r /tmp/restore/.hermes/ ~/.hermes/

# 還原 .upgrades/
cp -r /tmp/restore/.upgrades/ ~/.upgrades/

# 還原 projects
mkdir -p ~/projects
cp -r /tmp/restore/projects/ ~/projects/

# 還原 SSH keys
cp /tmp/restore/authorized_keys.txt ~/.ssh/authorized_keys

# 還原 packages (optional - install missing packages)
# sudo apt install -y $(cat /tmp/restore/packages.txt | awk '{print $1}')
```

### 6.4 還原 GG-Work

```bash
# 將 backup file scp 去 gg-work 或者直接喺 gg-work 上下載
tar xzf gg-work_full_YYYYMMDD_HHMM.tar.gz -C /tmp/restore

# 還原 skills
cp -r /tmp/restore/skills/ ~/skills/

# 還原 scripts
cp -r /tmp/restore/scripts/ ~/scripts/

# 還原 memory
cp -r /tmp/restore/memory/ ~/memory/

# 還原 workspace
cp -r /tmp/restore/workspace/ ~/workspace/

# 還原 dashboard
cp -r /tmp/restore/gg-dashboard/ ~/gg-dashboard/
```

### 6.5 還原 GG-Person

步驟同 GG-Work（同樣結構）。

### 6.6 還原敏感資料

backup 入面嘅 `.env` 同 token files 已包含 API keys：
```bash
# 設定正確權限
chmod 700 ~/.hermes/
chmod 600 ~/.hermes/.env
chmod 600 ~/.hermes/auth.json
chmod 600 ~/.hermes/drive_token.json
chmod 600 ~/.git-credentials  # 如有
```

---

## 7. 各 VM 專屬配置

### 7.1 GG Fighter (vmagc-00) 專屬

```bash
# 設定 cron jobs（從備份還原後自動回復）
crontab ~/.hermes/cron/crontab_backup.txt 2>/dev/null || echo "cron restored via hermes"

# Git credentials
# 手動設定 GitHub token（如有）
git config --global credential.helper store
echo "https://terrencelamkinet:YOUR_TOKEN@github.com" > ~/.git-credentials
chmod 600 ~/.git-credentials

# 重新啟動 Hermes Gateway
hermes start
```

### 7.2 GG-Work 專屬

```bash
# 安裝 nginx（如需 HTTP dashboard）
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# 設定 nginx config（從 backup workspace 還原）
# sudo cp ~/workspace/nginx-config/* /etc/nginx/sites-enabled/

# 啟用 UFW 加 port 80
sudo ufw allow from 172.6.15.0/24 to any port 80

# 重啟 OpenClaw gateway
# systemctl --user restart openclaw-gateway
```

### 7.3 跨 VM SSH 配置

```bash
# 確保三台 VM 可以互相 SSH
# 1. 每台 VM 嘅 public key 都要喺其他 VM 嘅 authorized_keys 度

# 快速設定（從 GG Fighter 執行）
ssh-copy-id airoot@gg-work
ssh-copy-id airoot@gg-person
# 喺 gg-work 同 gg-person 上都要做一次
```

---

## 8. 還原驗證清單

還原完成後，逐項 check：

- [ ] SSH 可連線到三台 VM（金鑰認證）
- [ ] 防火牆 UFW 已啟用（status: active）
- [ ] Python3 可執行（`python3 --version`）
- [ ] Node.js 可執行（`node --version`）
- [ ] Git 可 push/pull（`git pull` from ~/projects/ggdev-repo）
- [ ] Google Drive token 有效（`python3 ~/.local/bin/gg_backup.py list`）
- [ ] Notion API key 可連線（`cat ~/.config/notion/api_key` not empty）
- [ ] Telegram bot 可接收訊息
- [ ] Cron jobs 已註冊（`cronjob list`）
- [ ] 日誌系統正常（`journalctl -xe --no-pager | tail -20`）
- [ ] 磁碟空間足夠（`df -h | grep /$`）

---

## 附錄 A: Backup Script 用法

```bash
# 完整 backup（三台 VM）
python3 ~/.local/bin/gg_backup.py full

# 日常 data backup（三台 VM）
python3 ~/.local/bin/gg_backup.py data

# 列出所有 backup
python3 ~/.local/bin/gg_backup.py list

# 清理舊 full backup（keep 最新 8 個）
python3 ~/.local/bin/gg_backup.py cleanup
```

## 附錄 B: Backup 排程

| Cron Job | 時間 | 內容 |
|----------|------|------|
| Daily Data Backup | 每日 23:00 HKT | 核心 AI 資料（skills, memory, scripts, workspace） |
| Weekly Full Backup | 每週日 22:00 HKT | 完整 AI 環境 + 系統配置 + package list |
| Cleanup | Full backup 後自動執行 | 保留最近 8 個 full backup |

## 附錄 C: Google Drive 結構

```
GG_Backup/
  ├── 2026-05-30/
  │   ├── gg-fighter_full_20260530_1912.tar.gz    (248MB)
  │   ├── gg-work_full_20260530_1912.tar.gz       (1MB)
  │   ├── gg-person_full_20260530_1912.tar.gz     (1MB)
  │   └── _full_manifest.json
  ├── 2026-05-31/
  │   ├── gg-fighter_data_20260531_2300.tar.gz
  │   ├── gg-work_data_20260531_2300.tar.gz
  │   └── ...
  └── ...
```

---

## 附錄 D: 一鍵還原 (Recommended)

最快嘅還原方法 — 用 `gg_restore.py` script：

```bash
# 選項 1: 自動從 Google Drive 下載 backup
python3 gg_restore.py --drive 2026-05-30

# 選項 2: 手動下載 backup files 去 /tmp/gg-restore/ 再 run
# 下載 GG_Backup/ 入面最近期 full backup folder 嘅 3 個 tar.gz
# 放喺 /tmp/gg-restore/
python3 gg_restore.py
```

Script 會自動：
1. Detect 係邊部 VM（fighter / work / person）
2. 安裝 Ubuntu 工具 + Python + Node.js
3. 設定 SSH + 防火牆
4. 還原 AI 數據（.hermes / skills / memory / workspace）
5. 設定 Hermes Agent / OpenClaw
6. 驗證所有服務

Script 已放喺 `GG_Backup/gg_restore.py` — 同 backup 放埋一齊。

---

*Restore Guide v1.1 — GG AI Backup System*
*如有問題，聯絡 Terrence / Hermes Agent*

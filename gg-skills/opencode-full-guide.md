# OpenCode 系統深度解析與實戰攻略（完整版）

## 壹、四大運行形態

OpenCode 有四種形態：

### 1. CLI 命令行（最核心）
最完整版本，適合日常開發與進階操作。
安裝：`npm install -g @opencode/cli`
啟動：`opencode`

### 2. Desktop 客戶端
基礎對話框功能，Beta 階段。

### 3. VS Code 插件
需先安裝 CLI 版。
快速鍵：`Alt/Option + Shift + K` — 送 code 去 AI 聊天視窗，無縫關聯專案檔案。

### 4. GitHub Action（雲端整合）
將 OpenCode 變成 team 嘅 AI 協作者，直接喺 GitHub 雲端運行。

---

## 貳、系統安裝

### CLI 安裝（Node.js）
1. 安裝 Node.js（官網下載）
2. `npm install -g @opencode/cli`
3. `opencode` 啟動

### VS Code 插件
1. 確保 CLI 已安裝
2. VS Code 搜尋 "OpenCode" 安裝
3. `Ctrl/Cmd + Shift + P` → `OpenCode: Open`

---

## 參、模型接入

### 內建免費模型
指令 `/models` — 有 `free` 標記嘅即係免費

### Antigravity 插件（神級）
免費使用 Gemini 1.5 Pro + Claude 3.5 Sonnet
- 複製 GitHub 上嘅 prompt 貼入 OpenCode 自動安裝
- 新 terminal 執行認證 → 揀 Google → OAuth → 完成
- 重啟 OpenCode → `/models` 可選呢兩個 model

### OpenAI
ChatGPT 訂閱者可 login OpenAI 帳號用 GPT-4o

### OpenRouter
俾 API Key → 可用市面上幾乎所有大模型

---

## 肆、核心特性

### Session 並行開發
- 每個新對話 = 一個 Session
- `new` = 開新 Session 背景運行
- `/sessions` = 睇所有進行中 task（旋轉符號 = 背景運行緊）
- `/timeline` = 睇對話紀錄 + 修改點，可 Revert 回溯

### 拉爾夫循環 (Ralph Loop)
- 指令：`/r`
- 用途：超複雜任務，AI 自動循環直到完成
- 場景：重構成個 project、全部 test pass、數小時不間斷開發

---

## 伍、高階擴展

### Skills（技能包）
專案根目錄建立 `.opencode/skills/`  folder，放入 SOP。AI 遇到相關需求自動調用。

### MCP（Model Context Protocol）
修改 `~/.config/opencode/opencode.json`：
- **Local MCP**：如 shadcn，直接執行本地 script
- **Remote MCP**：如 ctx7（查最新文檔），填 URL + Header + API Key

### MyOpenCode（UltraW 模式）
整合工具 + MCP + 7 大專業 Agent（架構師、前端工程師等）。
- 魔法指令 `ultraw` → 主 Agent「西西弗斯」拆解 task → 動態調度子模型 → 多背景任務同時執行

### 自定義 Agent 與 Command
- **自訂指令**：`.opencode/commands/` 建立 `.md` 檔（如 `/run_tests`）
- **自訂 Agent**：`.opencode/agents/` 建立設定檔
  - `primary`：主智能體，可按 Tab 切換
  - `subagent`：子智能體（如 Code Reviewer），由主 AI 背景自動調度

---

## 陸、GitHub 工作流整合

1. 推專案上 GitHub
2. 專案中執行 OpenCode 安裝指令 → 揀 model → 自動生成 config
3. GitHub Repository Secrets 填 API Key
4. 團隊成員喺 Issue 留言 `@opencode 幫我修復導航欄嘅 bug`
5. OpenCode GitHub Action 雲端啟動 → 自動修 code → 發 PR

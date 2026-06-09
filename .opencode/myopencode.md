# MyOpenCode / UltraW Mode

整合工具 + MCP + 7 大專業 Agent 嘅終極開發模式。

## UltraW 模式

**魔法指令：** `ultraw`

當你輸入 `ultraw`，主 Agent「西西弗斯」(Sisyphus) 會：
1. 拆解 task 成細粒 subtask
2. 動態調度最適合嘅 sub-agent
3. 多個背景任務同時執行
4. 自動合併結果

## 7 大專業 Agent

| # | Agent | 專長 | Model |
|---|-------|------|-------|
| 1 | **Architect** 🏗️ | 系統設計、tech stack 決策 | DeepSeek V4 Flash |
| 2 | **Frontend Engineer** 🎨 | UI/UX implementation | Claude 3.5 Sonnet |
| 3 | **Backend Engineer** ⚙️ | API、database、business logic | DeepSeek V4 Flash |
| 4 | **Code Reviewer** 🔍 | Code quality、security audit | DeepSeek V4 Flash |
| 5 | **DevOps** 🚀 | Docker、CI/CD、deployment | DeepSeek V4 Flash |
| 6 | **Researcher** 📚 | API docs、best practices | Perplexity Sonar Pro |
| 7 | **Tech Writer** 📝 | Documentation、README | Claude 3.5 Sonnet |

## 整合工具

| 工具 | 用途 | 類型 |
|------|------|------|
| shadcn/ui | React component generation | Local MCP |
| Perplexity | Web search + research | Remote MCP |
| Notion | Project context | Remote MCP |
| Google | Calendar/contacts | Remote MCP |
| Design Lang | Design tokens | Remote MCP |
| rsync | Deploy to Mac Mini | Script |
| git | Version control | Built-in |

## 用法示例

```
ultraw 幫我整一個 user dashboard
```
→ 西西弗斯拆解：
  - Architect: 設計 dashboard 架構
  - Frontend: React component
  - Backend: API endpoints
  - Researcher: 查最新 chart library
  - Code Reviewer: 審查所有 code

```
ultraw 將 authentication system 加返 2FA
```
→ 西西弗斯拆解：
  - Architect: 設計 2FA flow
  - Backend: TOTP implementation
  - Frontend: 2FA setup page
  - DevOps: 更新部署 config

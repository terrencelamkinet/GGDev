---
name: opencode-model-strategy
version: 1
description: 智能 Model 切換策略 — 根據任務類型自動選擇最佳 AI 模型。Coding 用 DeepSeek V4 Flash / Gemini，UI design 用 Claude，Research 用 Perplexity。
summary: 按任務類型自動路由到最佳模型，最大化效率同準確度。
---

# OpenCode Model 切換策略

## 核心原則

**唔同任務唔同模型，唔好一個 model 走天涯。**

## Model Routing Matrix

| 任務類型 | 首選 Model | 備選 Model | 原因 |
|---------|-----------|-----------|------|
| **Code generation** | DeepSeek V4 Flash | Gemini 1.5 Pro | 最快最準嘅 code output |
| **Code review / refactor** | DeepSeek V4 Flash | Claude 3.5 Sonnet | 大 context window |
| **Bug fix / debug** | DeepSeek V4 Flash | — | 熟悉 codebase，速度快 |
| **UI design / component** | Claude 3.5 Sonnet | Gemini 1.5 Pro | Claude 對 UI 理解最好 |
| **API / library research** | Perplexity Sonar Pro | — | Search-grounded，確保最新 docs |
| **Architecture decision** | Perplexity Deep Research | — | 多源分析，全面考慮 |
| **Light task (typo/variable rename)** | DeepSeek V3.2 | — | 最平，夠快，夠用 |
| **Documentation** | Claude 3.5 Sonnet | Gemini 1.5 Pro | 寫作能力強 |

## 點解咁分配

### DeepSeek V4 Flash → Coding
- 對 code syntax 理解最深
- 生成 code 幾乎唔使改
- 大 context 可睇晒成個 project
- **免費**（via Antigravity）/ OpenRouter 低 cost

### Claude 3.5 Sonnet → UI Design
- 對視覺設計理解最好
- CSS/Tailwind 生成自然
- 擅長 component composition
- **免費**（via Antigravity）

### Perplexity → Research
- 每次回答都有 source citation
- 確保用嘅 API/library 係最新版本
- Deep Research mode 可以做全面分析
- 唔會亂 hallucinate API docs

### DeepSeek V3.2 → Light Tasks
- rename variable、fix typo 呢啲 trivial task
- 快、平、夠用
- 唔使浪費大 model quota

## 喺 OpenCode 嘅執行方法

### 方法 1：手動切換（Chat）
```
/model deepseek/deepseek-v4-flash    # 切去 coding model
/model claude-sonnet-3.5             # 切去 Claude
/model sonar-pro                     # 切去 Perplexity research
```

### 方法 2：喺 Prompt 指定
```
用 DeepSeek V4 Flash 幫我 generate 呢個 API endpoint...
用 Claude 幫我設計呢個 component 嘅 UI...
用 Perplexity 查吓 React 19 最新嘅 feature...
```

### 方法 3：Agent 自動路由（建議）
GG-Work Agent 會根據任務描述自動選擇 model：
- 「寫一個 FastAPI route」→ DeepSeek V4 Flash
- 「設計 landing page UI」→ Claude 3.5 Sonnet
- 「查吓 Stripe 嘅最新 API change」→ Perplexity Sonar Pro

## Antigravity 插件（免費 Model）

已安裝 Antigravity config，提供免費 model：
- **Gemini 1.5 Pro** — Google 提供，coding 同 reasoning 都唔錯
- **Claude 3.5 Sonnet** — Anthropic 提供，UI/Writing 最強

使用方法：
1. 確保已做 OAuth login（Google provider）
2. `/models` 見到 green check = 可用
3. 直接切換使用

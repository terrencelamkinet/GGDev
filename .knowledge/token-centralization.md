# 🔐 Token & API Key 中央化規則

## 鐵則
**所有 token / API key / secret / password 一律只存於 `~/.hermes/.env`（permission 600）**

嚴禁：
- ❌ Hardcode 喺任何 `.py` / `.sh` / `.json` / `.yaml` / `.md` file
- ❌ 寫落 git repo（包括 GGDev repo）
- ❌ 放喺 script 嘅 comment / docstring
- ❌ 喺任何 backup 出現（已 revoke 嘅除外）

## 點樣讀 token

### Python
```python
def get_token(name):
    env_path = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    return ""
```

### Shell
```bash
source ~/.hermes/.env
echo $TELEGRAM_BOT_TOKEN
```

## 目前中央化 token list

| Token Name | 用途 | 位置 |
|------------|------|------|
| `TELEGRAM_BOT_TOKEN` | GG Fighter Telegram bot | `.env` |
| `DEEPSEEK_API_KEY` | DeepSeek LLM API | `.env` / `auth.json` |
| `GOOGLE_MAPS_API_KEY` | Google Maps MCP + calendar | `.env` |
| `GOOGLE_CLIENT_ID` | Google Calendar OAuth | `.env` |
| `GOOGLE_CLIENT_SECRET` | Google Calendar OAuth | `.env` |
| `NOTION_API_KEY` | Notion API | MCP config `env` |
| `GITHUB_TOKEN` | Git push to DO | `.git-credentials` (600) |
| `SILICONFLOW_API_KEY` | Vision AI API | `.env` |

## Audit 檢查
每次自我審計檢查：
1. 所有 script 冇 hardcode token
2. `.env` permission = 600
3. `.env` 唔喺 git repo 入面
4. git remote 冇 embed token

## 紧急 revoke 流程
1. Bot token 洩露 → BotFather `/token` revoke
2. Google API key → Google Cloud Console
3. GitHub token → GitHub Settings
4. 任何懷疑洩露 → 立即 revoke + rotate

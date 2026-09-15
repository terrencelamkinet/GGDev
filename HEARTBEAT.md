# HEARTBEAT.md

## 🌅 晨間預讀（每日第一次對話自動執行）
當檢測到「呢個係一日內第一次同 Terrence 對話」時：
1. 讀取 `memory/patterns.md` → 喚醒 Terrence 嘅使用模式
2. 讀取 `memory/profile.md` → 喚醒個人設定
3. 讀取 `memory/$(date +%Y-%m-%d).md` → 今日嘅日記（如有）
4. 讀取 `memory/$(date -d 'yesterday' +%Y-%m-%d).md` → 尋日發生嘅事
5. 用一句話總結尋日狀況 + 今日準備好嘅狀態
6. 讀取 `.projects/_index.json` → 查看 active projects 清單，記錄到 context

### 每次對話（非 heartbeat）
- 用 `memory_search()` 快速 scan related context
- 如果話題涉及 active project，load 對應嘅 `.projects/<project>.json` 入 context

## 背景檢查（heartbeat 時執行）
- 每30分鐘檢查一次系統健康
- 留意緊急事項

## 保持空
如果冇特別任務，呢個檔案保持空，唔會觸發多餘 API 調用。

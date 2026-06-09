---
name: opencode-session-training
version: 1
description: Session 並行開發 + Ralph Loop 訓練指南。複雜 task 用 Ralph Loop，多獨立 task 用 Session 並行，出錯用 /timeline revert。
summary: 高效開發流程 — Session 並行、Ralph Loop 自動循環、Timeline revert。
---

# Session + Ralph Loop Training

## 核心工作流程

OpenCode 嘅 Session 系統同 Ralph Loop 係處理複雜 project 嘅兩大法寶。

---

## 1. Session 並行開發

### 咩係 Session？
每個新對話 = 一個 Session。你可以同時開多個 Session 背景運行。

### 點樣用？

| Instruction | 用途 |
|------------|------|
| `new` | 開新 Session，背景運行 |
| `/sessions` | 睇所有進行中 task（旋轉符號 = 背景運行緊） |
| `/timeline` | 睇當前對話紀錄 + 所有修改點 |
| `revert` | 回溯到修改前嘅版本 |

### 幾時用 Session？

**✅ 適合用 Session：**
- 多個獨立 task（例如同時寫 API + 前端 component）
- 需要等好耐嘅 task（例如大量 file generation）
- 唔相關嘅修改（唔會 conflict）

**❌ 唔適合用 Session：**
- 互相依賴嘅 task（一個改完另一個要用結果）
- 改同一個 file 嘅多個 task

### 最佳實踐
1. 見到有 2+ 個獨立 task → 用 `new` 開 Session 並行
2. 定期 `/sessions` check 進度
3. Session 完成後自動 merge 結果

---

## 2. Ralph Loop（/r）

### 咩係 Ralph Loop？
指令 `/r` → AI 自動循環執行超複雜任務，直到完成為止。

### 點樣用？
```
/r 幫我重構成個 authentication system
/r 將全部 test pass
/r 將呢個 monolith 拆做 microservices
```

### 幾時用 Ralph Loop？

**✅ 適合用 /r：**
- **超複雜任務（>5 files）** — 重構、重寫、migration
- **長時間任務** — 數小時不間斷開發
- **迭代優化** — 不斷改進直到滿意
- **全部 test pass** — AI 會 fix 所有 failing test

**❌ 唔適合用 /r：**
- 簡單 task（1-2 files）
- 只需要一次修改嘅 task

### Ralph Loop 限制
- 用 token 好多（不停循環）
- 可能陷入 infinite loop（要手動 `/stop`）

---

## 3. Error Recovery（Timeline + Revert）

### 出錯時嘅標準流程

```
Step 1: /timeline
  → 睇晒所有修改點
  → 搵出邊個 change 係 bug 來源

Step 2: Revert
  → 揀要退回嘅 checkpoint
  → 確認 revert

Step 3: 重新嘗試
  → 用更精準嘅 prompt 重新改
  → 或者用 Ralph Loop 自動 fix
```

### 點解用 Timeline 唔係 git？
OpenCode 嘅 Timeline 記錄每個 AI 修改點，粒度比 git commit 更細：
- 可以 revert 到某個 AI response 之前嘅狀態
- 唔會影響 git history

---

## 4. 實際場景

### Scenario A：重構成個 project（>5 files）
```
1. /r 重構 authentication system
2. 等 AI 自動循環修改
3. 中途 /sessions check 進度
4. 完成後 /timeline 確認所有修改
5. git commit + push
```

### Scenario B：多個獨立 task
```
1. 「幫我寫一個 user profile API」
   → 用 main session 做
2. `new` 「幫我設計 user profile 前端 component」
   → 開新 Session 並行
3. `/sessions` 睇兩個進度
4. 完成後 merge
```

### Scenario C：出錯修復
```
1. AI 改完發現 bug → 「嘩，壞咗」
2. /timeline → 搵 bug change
3. revert → 回到正常狀態
4. 重新 prompt（今次講清楚 constraint）
```

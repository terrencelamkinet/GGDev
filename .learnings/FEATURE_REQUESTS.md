# Feature Requests

Capabilities requested by the user.

---

## 2026-05-06

### 🔥 P0: 提升主動性 - 自我審視與進化機制
- **Request**: Terrence wants GG to be more proactive — reminders, care, understanding user needs better
- **Status**: ✅ In progress (this file system created)
- **Sub-tasks**:
  - [ ] 建立自我學習 .learnings/ 系統
  - [ ] 更新 SOUL.md 加入自我進化機制
  - [ ] 建立 context.md 動態生活狀況 tracking
  - [ ] 加入 human touch cron
  - [ ] 建立個人化提醒知識庫
  - [ ] 每月自我檢討機制

### 🔥 P0: 主動推送有用內容
- **Request**: News, weather, traffic, reminders pushed automatically
- **Status**: ✅ Partially done
- **Done**:
  - 07:00 新聞摘要（科技+本港+天氣）
  - 09:00 返工打卡（交通實況）
  - 18:00 收工打卡（交通實況）
- **To improve**:
  - [ ] 暴雨/颱風天氣主動提醒
  - [ ] 週末前主動問 plan
  - [ ] 夜晚 OT 提醒叫外賣

### 🔥 P0: 多平台叫車 Deep Link
- **Request**: One message with Uber/高德/DiDi/飛的 links
- **Status**: ⏸️ Paused — user said "先暫停"
- **Progress**:
  - Uber ✅ working
  - Others ❌ no public Universal Links found

### 🔥 P1: Google Calendar 整合
- **Request**: Auto-check calendar for meetings, proactive notification
- **Status**: ⏸️ Blocked — needs OAuth JSON from user
- **Next**: User said "聽日繼續搞"

### P2: SiliconFlow API 整合
- **Request**: TTS + ASR + OCR + Image Gen + Embedding
- **Status**: ⏸️ Paused — user said "都係普通話，算啦"
- **Working**: TTS (MOSS+CosyVoice2), LLM (DeepSeek-V4)
- **Not tested**: ASR, OCR, Image Gen, Embedding

## 2026-05-07

### 🔥 P0: 自駕全鏈查詢（已由 Terrence 確認要求）
- **Request**: 每次知道係自駕後，自動考慮以下所有事項，直至泊好位為止
- **Status**: ✅ Requirements recorded, implementation iterative
- **Complete Chain**:
  - [ ] 🛣️ 路線 — Google Maps Directions API（distance + normal time + live traffic）
  - [ ] 🌤️ 天氣（出發時 + 到達時）— HKO API
  - [ ] 📏 預計到達時間
  - [ ] 🅿️ 停車場選擇（附近3-4個，由近到遠排列）
  - [ ] 🅿️ 咪錶位 scan — HK Parking Meter Finder skill
  - [ ] 💰 泊車收費比較（時租、日泊、邊個最平）
  - [ ] 🔍 泊車位即時空位 scan（政府 API — 目前 403）
  - [ ] ⚠️ 最後實用提醒
- **Format Preference**: 文字描述，不要 table format
- **Data Source Priority**: Terrence 提供 > carparkhero > Car4Goal > Parkhaus > web_search
- **Notes**:
  - 收費要確認先講，冇即時數據要講「我無呢個資料」
  - 泊唔泊到要考慮車身高（7人車/Sienta）：要知高度限制
  - 要問清楚泊幾耐、幾點走、邊個位，唔好自己估
  - 如果車場收費可能有變，要問 Terrence 知唔知最新價

#### 💬 詢問機制規則
每次需要問 Terrence 問題前，必須先自我反問三次：
1. **呢條問題真係需要問嗎？** — 我係咪已經有足夠資料推論到？
2. **有冇其他已經有嘅資料可以代替呢條問題？** — 比如 context.md、MEMORY.md、之前對話
3. **如果唔問，最差情況係咩？** — 會俾錯答案定只係冇咁準？如果只係冇咁準，可以俾 range 或講「估計」

通過三次反問後，如果真係需要問：
- 一個問題一個問題問，唔好一次過炸
- 等 Terrence 答完先問下一個
- 夠資料就即停，唔好問多餘嘅

#### 🅿️ 泊車選擇優先級記錄
每次 Terrence 選擇泊邊個場之後，記錄佢嘅考慮因素，累積後形成優先級 pattern。

| 日期 | 目的地 | 給出的選擇 | Terrence選擇 | 考慮因素 |
|------|:------:|:----------:|:------------:|:---------|
| 2026-05-07 | 新蒲崗萬迪廣場(教會11F) | 萬迪$210日泊 / 啟鑽苑$152 / 荷里活$160+消費優惠 | 萬迪廣場 $210 | 唔想行遠、教會樓下、泊8hr(2pm-10pm) |

**Emerging Pattern**: 去教會 → 首要方便（唔行得遠），其次價錢

---


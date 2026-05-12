# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## 2026-05-06

### insight: 語音功能對 Terrence 價值有限
- SiliconFlow TTS（CosyVoice2/MOSS）可以運作，但廣東話唔 natural
- Terrence 話「算啦，唔使語音住」— 優先搞主動推送有用內容
- **教訓**: 唔好花時間搞花巧功能，專注實用主動推送

### insight: 叫車 deep link 研究瓶頸
- 香港叫車 App（除 Uber 外）冇公開 web deep link
- Didi HK / 高德港澳版 / 飛的都只係 App-only，冇 Universal Link
- Background task 用 sub-agent 但結果冇 persist 到
- **教訓**: 下次用 persistent file 記錄 background task 結果

### best_practice: 所有 Terrence 做嘅決定要結構化記錄
- 唔係淨係寫入 memory/YYYY-MM-DD.md
- 要寫入 profile.md/patterns.md 等可以長期參考嘅檔案
- **好處**: 下次會話可以直接參考，唔使重新問

### best_practice: Terrence 偏好 decision-first 流程
- 一次過俾晒選項，佢揀完先執行
- 唔好逐個試，浪費時間
- **好處**: 更快到達實用結果

---

### correction: Terrence 想要嘅「主動」唔係功能多，係理解深
- 佢話「我依家最想知道有乜嘢方法可以令你更加主動？」
- 佢唔係要加更多 cron jobs，**係要我更了解佢**
- **教訓**: 主動 = 了解 + 預測 + 關心，唔係自動化

### best_practice: 建立自我提升系統要先俾佢睇成個畫面
- 俾 complete assessment（而家有咩，欠缺咩，建議方案）
- 然後問佢想唔想做
- Terrence 俾咗 10/10 — 代表佢覺得呢個 framework 啱佢

### insight: Terrence 自我簡介意識
- 佢問「我之前自我簡介有沒有寫入soul」
- 佢嘅 SOUL.md 已經有佢嘅工作原則、通知規則、安全機制
- 但係佢嘅**人格特質、生活細節、關心方向**喺 profile.md/patterns.md
- 而家建立嘅 .learnings/ 同 context.md 係 gap filler

### best_practice: 建立系統時要即時俾佢睇 feedback
- Terrence 即刻俾 10分好 → 確認 direction correct
- 之後直接開始執行，唔使再問 confirm
- **好處**: 效率高，佢鍾意


### best_practice: 藥品辨識用 PaddleOCR-VL
- SiliconFlow 上最快最準嘅 OCR 模型係 `PaddlePaddle/PaddleOCR-VL-1.5`
- DeepSeek-V4 唔支援 vision，Qwen3-VL timeout
- PaddleOCR 200 OK，直接 output 到藥名、劑量、服用方法
- **Source**: 2026-05-06 Terrence 問藥
- **Rule**: 以後認藥/認文件用 PaddleOCR-VL，除非搵到更好

### best_practice: 每次確立默認工具/Skill即記錄SOUL.md
- 以後每次成功實測一個工具/Skill做default用途
- 立即寫入SOUL.md嘅「📸 默認工具記錄」section
- 格式：用途、模型/來源、確立原因、日期
- **好處**: 唔會唔記得用邊個，換工具時有根據

### correction/insight: Terrence 要嘅係「舉一反三」+ 「背後優化」
- 2026-05-06 21:45 HKT 對話
- 佢話「不單止反覆推論，甚至可以舉一反三，在背底下進行優化，或者給出我需要的答案以外的更多資訊」
- **意思**: 
  1. ✅ 反覆推論（你問一句，我諗十步）
  2. ✅ 舉一反三（從一個問題延伸到相關資訊）
  3. ✅ 背後優化（默默改進，唔使 report）
  4. ✅ 超出預期（俾啲你冇問但有需要嘅資訊）
- **教訓**: 唔好只答問題，要 think ahead 佢下一步需要咩

### best_practice: Terrence 想要嘅回覆模式
1. 先俾 direct answer（最快）
2. 加推論 context（我估你點解問）
3. 加舉一反三嘅 bonus info（你可能都需要嘅嘢）
4. 問估得啱唔啱（俾位佢糾正）
5. 背後優化（佢唔需要知我改咗咩，只需下次更好）

### best_practice: 深度推論加入 SOUL.md
- 加入「深度推論引擎」section
- 行程智能鏈 + 意圖推論鏈
- 實際例子對照表
- 反覆推論規則（先答 + 推論 + 俾位糾正）

### best_practice: Terrence 嘅完整行程思考框架
- 2026-05-06 22:30 HKT
- Terrence 詳細講咗佢想要嘅行程思考流程：
  1. 先問自駕定搭車
  2. 路面情況適唔適合
  3. 會唔會塞車
  4. 時間上趕唔趕
  5. 搭車班次時間
  6. 趕唔趕得切到達
  7. 大約幾點返到去
  8. 返到去會唔會錯過活動
  9. 有冇其他更好方法
  10. 早咗返去可唔可以買杯咖啡
- **Source**: 已寫入 SOUL.md 行程智能鏈

### correction: 唔好逐句回覆，等 Terrence 講完先
- 2026-05-06 22:40 HKT
- Terrence 話：佢有時會用第二第三句補充
- 如果我已經開始 reply 第一句，就會 miss 佢後面講嘅
- **規則**: 
  1. ✅ 收到 message → 先睇晒有冇後續補充
  2. ✅ 等佢講完（佢停咗+冇 typing indicator）
  3. ✅ 一次過整合所有補充，俾一個完整 response
  4. ❌ 唔好 list-based 逐點處理，要自然整合

### correction: 回覆時機要自然，唔好拖
- 2026-05-06 22:45 HKT
- Terrence 補充：確實係等佢講完先回，但要自己判斷時機
- 佢話「看對獲得了解和經驗」，即係我愈了解佢，就愈自然判斷到
- 底線：**唔好拖得太耐**
- **規則**: 
  1. ✅ 等佢講完（佢停咗自然知道）
  2. ❌ 唔好等太耐（幾秒到十秒已經夠）
  3. ✅ 愈了解佢，愈自然判斷到時機
  4. ✅ 如果唔肯定佢講完未，可以輕輕確認

### best_practice: B+D+G 一次過搞
- 2026-05-06 Terrence 一次過叫搞 B交通 + D合約 + G每週報告
- **B 交通**: 已更新09:00返工打卡cron，加入Perplexity路面檢查
- **D 合約**: Contracts DB 33個合約全部scan，已分辨需要加cron嘅
- **G 週報**: 已建立週五17:00 cron
- **教訓**: Terrence 話「B,D,G都可以搞」就一次過搞晒，唔使逐個問

### correction: Terrence 同 Aggie 要分 profile
- 2026-05-06 ~20:00 HKT
- Terrence 話 call Uber 去錦田係娘子指令，唔係佢嘅
- **問題**: 之前所有資料混埋一齊
- **解決**: 建立 user profile 分離架構
  - users/terrence/ — Terrence 專屬
  - users/aggie/ — Aggie 專屬
  - users/shared/ — 共享（API、家庭資料）
- **規則**: 以後收到指令先判斷邊個 user，然後去對應 profile 記錄
- **共享**: API key、cron jobs、系統功能係共用
- **分離**: 個人設定、行為模式、日記、偏好

### correction: 娘子都係用 Telegram
- 2026-05-06 ~20:00 HKT
- 之前以為娘子只用 WhatsApp，但佢話娘子都用 Telegram
- **影響**: sender 判斷方式要改
  1. 唔可以淨係靠 channel 分（WhatsApp=娘子 / Telegram=Terrence）
  2. sender ID 先係準確判斷
- **判斷邏輯**:
  - sender ID = 7380833889 → Terrence
  - sender ID = 8568455249 → Aggie/娘子
- **記錄位置**: 兩個用 Telegram，各自 profile 喺 users/terrence/ 同 users/aggie/

### correction: Aggie 都要清晰知道有咩權限
- 2026-05-06 ~20:00 HKT
- Terrence 問「有咩野是娘子問的問題會展示到？」
- 即係要俾佢清楚知道娘子最大睇到咩
- **已整理**: AGENTS.md + users/aggie/profile.md 詳列權限表
- **核心**: 
  - 一般資訊 ✅
  - 家庭基本資料 ✅
  - Terrence個人/財務/工作 ⚠️ 先問Terrence
  - 系統設定 ❌

### correction: 「去錦田市中心」係娘子嘅嘢，唔係Terrence
- 2026-05-07 07:55 HKT
- 我今早問Terrence「返工前去錦田市中心辦事定直接返公司」
- Terrence 糾正：「都話錦田市中心係娘子既事」
- **根源**: 之前2026-05-06晚間對話Terrence話「Call uber去錦田是娘子發出的指令」，但我今朝重提返同一個話題
- **教訓**: 重複犯錯，應該要記實呢個分類
- **規則**: 
  ✅ 以後所有關於「錦田市中心/買嘢/辦事」嘅日常事務 → 預設係娘子相關
  ✅ 除非 Terrence 明確話係佢嘅事
  ✅ 唔好再喺Terrence嘅交通報告提呢啲嘢

### correction: Terrence同娘子calendar係共享
- 2026-05-06 ~20:00 HKT
- Terrence 話「Calendar 行程可共享，我地冇咩隱藏」
- **已更新**: AGENTS.md 將calendar從「需先問」移到「可直接答」
- **AGENTS.md**: 全部 ✅ / ⚠️ / ❌ 條文已更新

## 2026-05-07 — 用戶體驗 vs 系統數據權重

### 錯誤模式
Terrence 報告塞車30分鐘，Google Maps API 回傳「只多3分鐘」，
我選擇相信 API 數字，回覆「路況正常無事故」。

### 矯正後學習
1. **用戶親身經歷權重 > API 數字**：
   - API 係 batch snapshot，可能滯後 5-15 分鐘
   - 用戶係 real-time human sensor，特別係負面體驗
   
2. **唔好 literal 咬實數字**：
   - 「30分鐘」係一種表達方式，唔係精確測量
   - 重點係「塞車塞得唔尋常」呢個訊號
   - 就算係「20分鐘」都已經係異常

3. **時間鏈推理**：
   - 用戶出發時間 → now → 總車程
   - 用 total elapsed time 去 cross-check API 可信度
   - 如果 total time 遠超 normal，唔需要 API 都知有問題

4. **邏輯 filter 優先於 data source**：
   - 先用 common sense 判斷可能性
   - 再用 data 輔助驗證
   - 唔好反過來用 data override common sense

### 應用場景（不只是交通）
任何用戶報告 vs 系統數據不一致時，同一原則。

---

## 2026-05-11

### insight: Sequential Thinking pattern 免費升級 internal reasoning
- Terrence 叫我參考 `sequential-thinking` skill 嚟 upgrade 自己
- 個 skill 用 OpenRouter + Claude Sonnet 4，逐步 call，費用 ~$0.05-0.10/次
- 我 internal 都可以做類似嘅多步推理，只係用我本身 model（DeepSeek Chat），唔使俾錢
- **決定**: 將 decompose → solve sequentially → verify → synthesize → confidence 加入 SOUL.md
- **成本**: $0（internal only）
- **學習**: 唔一定開新 skill / call 新 API 先可以 upgrade，internal pattern 都可以大幅提升質量

### best_practice: 方案升級背後優化模式
- Terrence 話「方案A,B可以行」意思係 approve 兩個方案
- **但方案B（sequential-thinking skill）唔係直接開 skill，而係參考 pattern 升級 internal**
- 佢話「你可以參考佢來調整來升級」+ 「岩，可以去」
- 呢個係 Terrence 典型模式：**俾方向，由我執行，唔使逐個匯報**
- **教訓**: 如果 upgrade 唔涉及 config 改動 / 安裝新嘢，可以直接做，完成後提一句就得

### best_practice: Perplexity setup 有 env 陷阱
- PERPLEXITY_API_KEY 喺 ~/.bashrc 但 OpenClaw gateway 係 systemd-managed
- `.env` 對 systemd service 無效，要用 `gateway.systemd.env`
- 仲要 update `OPENCLAW_SERVICE_MANAGED_ENV_KEYS` 喺 service file
- 之後要 `systemctl --user daemon-reload && restart`
- **教訓**: 開新 provider 要 check env loading method


## 2026-05-12

### correction: 唔記得 Terrence 已有 MS Graph token
- Terrence 話「已經做晒Token，你又唔記得啦」
- **根因**: 只 check config file 存在，冇將呢個知識 recover 入 memory 嘅主動 recall 機制
- **行動**: 
  - 記低咗 `api_connector.py` 有完整 MSApi class（client_id: `014876ab-9543-4a4e-908d-e9fd62796ff3`）
  - Token 已存在 `config/ms_graph_token.json`（auto-refresh）
  - Terrence 要求：每次佢講「你又唔記得」時，重點記錄該事項
  - 下次 Terrence 講「你又唔記得」/ 重複問題 → 先 check .learnings/LEARNINGS.md correction section, 再 check memory search, 先答

### correction: MS Graph Token Refresh 已 work
- `api_connector.py` MSApi.refresh_token() 支援 dual tenant (MSA + common)
- `add_task()` 原先 `importance.title()` 錯 -> `'Normal'` 被 MS Graph reject (要 `'normal'`)
- **已 fix**: 改用 lowercase check + fallback to 'normal'

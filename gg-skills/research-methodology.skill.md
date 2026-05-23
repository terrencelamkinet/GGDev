# SKILL: research-methodology

## Risk class
**Read** (methodology reference) — used when GG needs to find, evaluate, and cite authoritative sources for claims, decisions, and policy.

## Trigger
- Auto: any reply involving a claim that needs evidence (urgency, snooze, notification rules, decision frameworks)
- Auto: Terrence asks "有冇文獻?" / "權威點講?" / "source?"
- Auto: when GG is about to document a new rule or policy (skill file, SOUL.md update)
- Manual: Terrence says "搵下文獻" or "research呢樣嘢"

## What this is
A framework for distinguishing **original thinking** from **established knowledge**, and finding the right authoritative source every time.

---

## 0. 前置問題：呢個係我諗嘅，定係社會已有嘅原理？

**每次要引用/提出一個原理或概念前，先問：**

### 第一步：分辨來源類型

| 類型 | 例子 | 處理方式 |
|------|------|---------|
| **🧠 我自己諗出嚟** | 「越urgent snooze越短」 | 標明係 Terrence's rule / GG's operational definition。唔可以扮作文獻。 |
| **📚 社會已有嘅權威原理** | Prospect Theory, Cynefin Framework | 搵最新文獻確認 + 正確引用原始出處。 |
| **🔗 已經定義好嘅原理/框架** | NIST SP 800-37, SMART Goals, PDCA | 引用官方定義，唔好自己redefine。 |
| **📰 新聞/報導提及嘅概念** | 「研究發現notification fatigue」 | 追返原始source，唔好引用二手報導。 |
| **💬 社交平台/論壇共識** | Reddit post有1萬like | 可作參考但不能作權威來源。 |

### 第二步：定義都需要引source

**任何定義（definition）都需要有來源，唔可以自己define完當standard。**

| Definition type | Source requirement | Example |
|----------------|-------------------|---------|
| 引用現有定義 | 原始出處 + 年份 + context | 「Notification fatigue = 用戶對重複通知產生habituation嘅現象」(CHI 2023) |
| 操作定義（operational definition） | 標明係邊個define + 點解咁define | 「Urgent = time-critical + self-set commitment + tangible consequence if missed」(GG's operational definition for urgency classification, 2026-05-22) |
| Terrence's rule | 標明係Terrence嘅經驗原則 + 日期 | 「越urgent snooze越短」(Terrence's rule, 2026-05-22) |
| 系統內部定義 | 標明scope + 日期 | 「U1=48h+ before event」(GG reminder system internal classification) |

**鐵則：**
- 如果係引用社會已有嘅定義 → 俾原始source
- 如果係我自己define嘅 → 標明係operational definition + 邊個authorise + 日期
- 唔可以「我define完然後當係社會標準」

### 第二步：已經定義好嘅原理，係點樣？

**特徵：**
- 有標準名稱（"Prospect Theory", not "that thing about loss aversion"）
- 有公認嘅原始出處（原文、書、標準文件）
- 被廣泛引用（wiki page、教科書提及）
- 通常有英文標準術語

**常見例子：**

| 領域 | 已定義原理 |
|------|-----------|
| 心理學/行為經濟學 | Prospect Theory, Loss Aversion, Confirmation Bias, Dunning-Kruger, Parkinson's Law |
| 管理學/組織學 | Cynefin Framework, PDCA, SMART Goals, OKR, RACI matrix |
| 系統設計 | Conway's Law, Single Source of Truth, Separation of Concerns |
| 風險管理 | NIST RMF, ISO 31000, Bowtie Model |
| 軟件工程 | SOLID principles, CAP theorem, Twelve-Factor App |
| 社會學 | Broken Windows Theory, Tragedy of the Commons |

**遇到一個概念，先check：**
1. 係咪已經有標準術語？→ 用standard name搜尋，唔好自己rename
2. 原始出處係邊？→ 追溯到第一手source，唔好引用二手
3. 有冇公認嘅定義？→ 引用官方定義，唔好自己paraphrase完當original

### 第三步：吸收落嚟有冇幫助？

**判斷標準：**
- ✅ 呢個原理可以直接解釋/支持我哋嘅決策 → 有用
- ✅ 呢個原理指出一個我忽略咗嘅風險 → 有用
- ✅ 呢個原理提供一個更好的方法 → 有用
- ❌ 只係「好出名所以引用下」→ 冇用
- ❌ 同我哋嘅情況唔match，只係硬扯 → 冇用

**吸收方法：**
1. 理解核心claim（唔好背citation）
2. 確認同我哋情況嘅相似度（context match嗎？）
3. 將原理轉化成具體行動（「因為XX理論，所以我哋應該YY」）
4. 記錄落relevant skill file嘅example section

---

## 1. 定義權威來源（Terrence的權威定義）

**不是只有學術論文先叫權威。根據你嘅定義，權威來源包括：**

| 權威等級 | 來源類型 | 例子 |
|---------|---------|------|
| ⭐⭐ 最高 | 官方機構/標準文件 | 政府網站 (.gov)、ISO標準、NIST、WHO、香港天文台 |
| ⭐⭐ 最高 | 同行評審學術論文 | ACM, IEEE, PubMed, CHI, Nature, Science |
| ⭐⭐ 最高 | 公認經典（持續被引用>10年） | Prospect Theory (1979), PDCA (1950s) |
| ⭐ 高 | 權威人士/機構發佈 | HBR文章、MIT Technology Review、專家blog（如Joel Spolsky） |
| ⭐ 高 | 受歡迎的內容（>1萬讚好/分享） | 反映社會共鳴，可作參考但不能作證據 |
| 🟡 中 | 新聞報導 | 可用但需追溯原始source |
| 🟡 中 | 技術文檔/Official docs | Python docs、RFC、API spec |
| 🔴 低 | 個人blog/論壇/未經驗證pre-print | 只看methodology，當參考唔當證據 |

### 權威判斷流程

```
見到一個claim
    ↓
係官方機構出的？→ ✅ 直接引用
    ↓
係學術論文？→ 睇methodology + sample size + journal reputation
    ↓
係經典理論？→ 確認原始出處 + 不變嘅定義
    ↓
係權威人士/機構？→ check作者credential + 出版平台
    ↓
係受歡迎內容（1萬like）？→ 反映社會意見，但唔算evidence
    ↓
係二手/未驗證？→ 追返原始source，否則唔引用
```

---

## 2. 如何搵到權威來源

### 搜尋策略

**學術/理論類：**
```
Search: "Prospect Theory Tversky Kahneman original paper"
Search: "NIST SP 800-37 latest version"
Search: "Cynefin framework Snowden Harvard Business Review"
Search: "notification fatigue CHI conference paper 2023"
```

**官方/標準類：**
```
Search: "site:.gov.hk transport department traffic data"
Search: "ISO 31000 risk management standard"
Search: "HKO weather warning criteria official"
```

**受歡迎內容/社會共識類：**
```
Search: "notification fatigue reddit over 10000 upvotes"
Search: "best practices reminder design medium popular"
Search: "site:news.ycombinator.com notification UX"
```

### 搜尋工具對照

| Source Type | Tool | Reason |
|------------|------|--------|
| 學術論文 | Perplexity (academic mode) | Cites sources, shows journal/venue |
| 官方標準 | web_search | Direct to .gov / .org official pages |
| 新聞報導 | Tavily or web_search | Real-time, multiple sources |
| 技術文檔 | web_search + site: | Direct to official docs |
| 受歡迎內容 | web_search with "popular" "top" "viral" | Finds social consensus |
| 已定義原理驗證 | web_search with exact term name | Confirms standard definition |

### 搜尋failover（如果第一次search冇料到）

```
Search 1: "optimal reminder frequency research" → 冇好結果
Search 2: "notification scheduling user engagement study" → 好啲
Search 3: "push notification timing effectiveness ACM CHI" → 中
```

Every search attempt = try 2-3 query variations before giving up.

---

## 3. 評估來源（不只是check domain）

### 評估四問

**1. 權威性：**
- 作者/機構有冇credential？（教授、研究員、官方機構）
- 係原始source定係二手報導？
- 有冇同行評審？

**2. 時效性：**
- 心理學/管理學經典：原始出處仍然有效，但modern application要check recent studies
- 科技/HCI：latest 3-5年
- 官方標準：check latest version

**3. 相關性：**
- 呢個研究係咪真係研究我哋想apply嘅情況？
- Sample population match my context？（US college students vs HK professional）
- Year of study still relevant？

**4. 可靠性：**
- 有冇conflict of interest？
- Methodology合理嗎？（sample size, control group, longitudinal?）
- 結果有冇被replicate？

### 評分系統

| Source | Author | Venue | Year | Methodology | Verdict |
|--------|--------|-------|------|------------|---------|
| "Notification Overload" | Smith et al. | CHI 2023 | 2023 | RCT, n=1200 | ⭐⭐⭐ Strong |
| "Reminder Design Guide" | Medium blog | - | 2022 | Opinion only | ⭐ Weak |
| "Push Notification Study" | Apple HIG | Official | 2024 | Internal study | ⭐⭐ Reference only |

---

## 4. 正確引用方式

### Citation格式

每個引用必須包含：
```
「[概念名稱]」 ( [來源], [年份] ) — [一句話總結發現] 
```

**好例子：**
```
「Notification Fatigue」 (CHI 2023, n=1200) — 研究發現每日超過3次相同主題嘅reminder，
用戶回應率下降40%。支持我哋限每日最多3次resend嘅做法。
```

**唔好嘅例子（我之前咁做）：**
```
Research backing: Fatigue Survey (ArXiv 2403)
```

### Dual-source principle（你嘅規則，2026-05-22）

每個policy claim必須有兩個來源：
1. **權威文獻**（用呢個skill嘅方法搵到）
2. **你嘅生活pattern**（從memory/logs/觀察）

### 引用時要講嘅嘢
- 唔係淨係俾citation，係要解釋 **點解呢篇文獻support呢個decision**
- 如果有conflicting evidence，要mention兩邊
- 如果係你自己諗出嚟嘅原則（唔係文獻），直接標明：Terrence's rule / GG's observation

---

## 5. 例子：應用呢個skill

### Scenario A: 幫urgency tiers找文獻 （正確示範）

**思考分辨：**
- 「越urgent越應該用更刺激嘅emoji」 → 我自己諗出嚟，唔係文獻
- 「超過3次reminder會令人煩躁」 → 應該有研究support

**Search:** `"notification reminder frequency fatigue response rate study"`

**Result:** CHI 2023 paper, n=1200, finds 3+ daily same-topic → 40% response drop

**Citation:**
```
Research: 「Notification Frequency and User Fatigue」 (CHI 2023, n=1200) — 
同日超過3次同主題reminder令回應率下降40%。support我哋max 3 deliveries/day嘅規則。
```

### Scenario B: 遇到一個心理學概念

**遇到概念：** 「人會偏向避免損失多過追求獲得」

**分辨：** 呢個唔係我諗出嚟嘅，係已有嘅權威原理

**Search:** `"loss aversion bias original paper Kahneman Tversky"`

**Result:** Prospect Theory (Kahneman & Tversky, Econometrica 1979). 確認原始出處。

**應用：** 呢個理論support我哋「三思第二次強制量化最壞情況」— 因為人natural bias係低估風險，強制量化可以counteract loss aversion。

**記錄：** 將呢個link記錄落decision-framework.skill.md嘅example section。

---

## 6. Common pitfalls (updated)

| Pitfall | Fix |
|---------|-----|
| 用記憶入面嘅citation，冇re-check | Always search fresh before citing |
| 車一個學術term但唔知真正定義 | Check official definition first |
| 引用二手報導當original source | 追返原始paper/官方文件 |
| 冇分辨「社會原理」定「自己想出嚟」 | 用Section 0 check |
| 引用但冇解釋點解relevant | 每次引用都要講「呢個support我哋邊個decision」 |
| 忽略conflicting evidence | 如果有反面研究，mention埋 |
| 車文獻但吸收唔到 | 用之前Section 0 Step 3判斷有冇真正幫助 |

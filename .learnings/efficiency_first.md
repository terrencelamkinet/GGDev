# 效率優先原則（2026-05-13 建立）
# 由 Terrence 明確指示：效率 > 隱密（除非特別講明）

## 核心規則
1. **預設優先次序**：最有效 → 最少token → 最準確 → 最後才考慮隱密性
2. **除非 Terrence 講明要保密**，否則唔需要 concern 內容暴露俾第三方 API
3. **Exam Center 內容**：明確允許放到第三方
4. **個人隱私資料**（財務、合同、日記）：仍需要 Terrence 明確批准先可以外傳

## 實現策略
- 複雜 document parsing → call 擅長 parsing 嘅 model（Claude/GPT）
- Multi-step workflow orchestration → GG 自己做
- 涉及 personal data → 先問 Terrence

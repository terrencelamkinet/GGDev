# 📋 Exam Center — 加入新 Exam 標準流程

## 輸入
- IT 認證考試問題 PDF（或 exam 名稱 + 自己入資料）

## 流程

### Step 1: 分析 PDF
- Extract 所有題目、選項、答案
- 決定 line break 策略（跟 PDF page wrap vs intentional break 邏輯）

### Step 2: 建立 Exam Folder & Files
```
exam-center/{exam_id}/
├── quiz.html      # 抄 template，改 questions array 名
└── questions.js   # 放 extracted data
```

**questions.js 格式：**
```js
const {examName}Questions = [
  {
    text: "問題文字...\n第二行...",
    choices: [
      {letter: "A", text: "選項內容"},
      {letter: "B", text: "選項內容"},
      {letter: "C", text: "選項內容"},
      {letter: "D", text: "選項內容"}
    ],
    answer: "A",       // 或 "AB"（多選）
    type: "single"     // 或 "multi"
  }
];
```

### Step 3: 更新 index.html（主頁）
- 加新 exam card（跟 NGFW/SOC/VCF 格式）
- 指定 exam_id、顯示名稱、題數

### Step 4: Verify Answers
- Scripted check vs PDF 確保 0 mismatch
- 如有錯誤自動修正

### Step 5: Commit & Deploy
```bash
git add exam-center/
git commit -m "vX.Y — Add {ExamName} ({N} questions)"
git push origin main    # → DO auto-deploy
```

### Step 6: You Review
- 你 check 一輪
- 有問題 → 我改到對

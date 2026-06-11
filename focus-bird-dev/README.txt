===========================================
  專注飛鳥 Pro (Focus Bird Pro) v3
  腦電波專注力訓練遊戲
===========================================

【檔案說明】
  game/
    focus-bird-pro.html     主遊戲檔案，用瀏覽器開啟即可

  bridge/
    focus_bridge_windows.py  Windows BrainLink 連接程式
    requirements.txt         Python 套件需求
    setup_windows.bat        一鍵安裝 Python 套件
    start_bridge.bat         啟動腦電波橋接器

【快速開始】

  Step 1: 安裝 Python 3.10+
    https://www.python.org/downloads/

  Step 2: 安裝套件
    雙擊 bridge/setup_windows.bat

  Step 3: 下載 BrainLinkParser
    前往 https://www.macrotellect.com/web/mobile/developer.html
    下載 BrainLinkParser.py 並放入 bridge/ 資料夾

  Step 4: 連接 BrainLink 頭盔
    透過藍牙或 USB 連接 BrainLink 頭盔到電腦

  Step 5: 啟動橋接程式
    雙擊 bridge/start_bridge.bat
    輸入對應的 COM port（例如 COM5）

  Step 6: 開啟遊戲
    用 Chrome 或 Edge 開啟 game/focus-bird-pro.html
    遊戲頁面右上角圓點變綠色 = 連接成功

【遊戲說明】
  - 專注度高時小鳥下沉，收集地上食物
  - 共10層，每層10關，共100關
  - 第1層：蘋果 / 第2層：粟米 / 第3層：薯條
  - 第4層：可樂 / 第5層：甜品 / 第6層：朱古力
  - 第7層：雪糕 / 第8層：蛋糕
  - 第9層：雙重混合 / 第10層：終極混合
  - 年齡設定：1至40歲，自動調整難度
  - 無頭盔時可按 Space 鍵測試

【一個月訓練計劃】
  遊戲內「一個月訓練計劃」按鈕可查看詳細方案。
  建議頻率：每週3-5次
  每次時長：按年齡×2-3分鐘（例如6歲=12-18分鐘）
  參考依據：美國兒科學會、PMC 2025年研究、NHA指引

【技術規格】
  遊戲畫面：1920 × 1024（自動適配螢幕）
  腦電波協議：BrainLink WebSocket ws://localhost:8765
  資料格式：{"attention": 0-100, "meditation": 0-100, ...}
  瀏覽器：Chrome 90+ / Edge 90+ 推薦

【WebSocket 自訂連接】
  遊戲網址加入參數：
  file:///path/to/focus-bird-pro.html?ws=ws://192.168.1.x:8765

【聯絡支援】
  BrainLink SDK: https://www.macrotellect.com/web/mobile/developer.html
===========================================

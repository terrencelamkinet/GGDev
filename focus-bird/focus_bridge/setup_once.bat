@echo off
REM ============================================
REM  BrainLink Bridge — 一次性設定 (setup_once.bat)
REM  適用：Windows (Lenovo X1)
REM  用途：確認 Python 3.11、安裝 deps、掃描 COM port
REM ============================================
setlocal enabledelayedexpansion
echo ============================================
echo   🧠 BrainLink Bridge — 一次性設定
echo ============================================
echo.

REM ---- Step 1: Check Python ----
echo [1/4] 檢查 Python 版本...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 未安裝 Python！
    echo    請安裝 Python 3.11: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version 2>&1 | find "3.11" >nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  當前 Python 版本可能唔係 3.11
    python --version
    echo.
    echo    BrainLinkParser.pyd 只兼容 Python 3.11！
    echo    如果仲未安裝 3.11，請去 https://www.python.org/downloads/
    echo.
    choice /C YN /M "繼續 (Y) 或 取消 (N)"
    if !ERRORLEVEL! EQU 2 exit /b 1
) else (
    echo ✅ Python 3.11 確認
)
echo.

REM ---- Step 2: Install dependencies ----
echo [2/4] 安裝依賴...
pip install cushy-serial websockets pyserial
if %ERRORLEVEL% NEQ 0 (
    echo ❌ pip install 失敗
    pause
    exit /b 1
)
echo ✅ 依賴安裝完成
echo.

REM ---- Step 3: Check BrainLinkParser.pyd ----
echo [3/4] 檢查 BrainLinkParser.pyd...
if exist BrainLinkParser.pyd (
    echo ✅ BrainLinkParser.pyd 存在
) else (
    echo ⚠️  BrainLinkParser.pyd 未找到！
    echo    請手動下載：
    echo    https://github.com/Macrotellect/BrainLinkParser-Python
    echo    → Windows 資料夾 → BrainLinkParser.pyd (Python 3.11 版本)
    echo    然後放喺本目錄 (同 brainlink_bridge.py 同一層)
)
echo.

REM ---- Step 4: Scan COM ports ----
echo [4/4] 掃描藍牙 COM Port...
python brainlink_bridge.py --scan
echo.
echo 💡 記低你嘅 Outgoing COM port（例如 COM5）
echo    然後編輯 config.txt 設定
echo.

REM ---- Create config.txt if not exists ----
if not exist config.txt (
    echo Creating default config.txt...
    (
        echo # BrainLink Bridge Config
        echo # 請修改 COM port 同 Agent Server URL
        echo BLUETOOTH_COM=COM5
        echo AGENT_WS_URL=wss://your-agent-server.com:8765/brainlink
    ) > config.txt
    echo ✅ config.txt 已建立，請編輯
)

echo ============================================
echo   ✅ 設定完成！
echo   下一步：編輯 config.txt，然後 run start_bridge.bat
echo ============================================
pause

@echo off
REM ============================================
REM  BrainLink Bridge — 啟動 Bridge (start_bridge.bat)
REM  適用：Windows (Lenovo X1)
REM  用途：讀取 config.txt，啟動 brainlink_bridge.py
REM ============================================
setlocal enabledelayedexpansion
echo ============================================
echo   🧠 BrainLink Bridge — 啟動
echo ============================================
echo.

REM ---- Check config.txt ----
if not exist config.txt (
    echo ❌ config.txt 未找到！
    echo    請先執行 setup_once.bat 或手動建立 config.txt
    pause
    exit /b 1
)

echo 📄 讀取 config.txt...
type config.txt
echo.

REM ---- Read config values ----
for /f "tokens=1,2 delims==" %%a in (config.txt) do (
    if /i "%%a"=="BLUETOOTH_COM" set COM_PORT=%%b
    if /i "%%a"=="AGENT_WS_URL" set WS_URL=%%b
)

if "%COM_PORT%"=="" (
    echo ❌ config.txt 缺少 BLUETOOTH_COM
    pause
    exit /b 1
)

if "%WS_URL%"=="" (
    echo ⚠️  config.txt 缺少 AGENT_WS_URL
    echo    將使用 local mode (直接 broadcast 俾 browser)
    echo.
    python brainlink_bridge.py --port %COM_PORT% --local
) else (
    echo 🚀 啟動 Bridge...
    echo    COM Port: %COM_PORT%
    echo    Agent URL: %WS_URL%
    echo.
    python brainlink_bridge.py --port %COM_PORT% --url %WS_URL%
)

echo.
echo 👋 Bridge 已關閉
pause

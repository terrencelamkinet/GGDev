@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo   Focus Bird v3 - Loading...
echo   Make sure BrainLink headset is ON.
echo ========================================
echo.
echo [1/3] Starting BrainLink Bridge...
start /min cmd /c py -3.11 brainlink_pro.py --port COM3 --relay
timeout /t 3 >nul
echo.
echo [2/3] Waiting for device (max 60s)...
:wait_loop
echo [..] Checking relay...
py -3.11 health_check.py >nul 2>&1
if %ERRORLEVEL%==0 (
    echo [OK] Device ready!
    goto open
)
if %ERRORLEVEL%==2 (
    echo [--] Bridge not connected yet, retrying...
    timeout /t 3 >nul
    goto wait_loop
)
echo [--] No signal yet (sig>=150), waiting...
timeout /t 3 >nul
goto wait_loop

:open
echo.
echo [3/3] Opening game...
start "" chrome "https://focus-bird.kinet-poc.com/focus_bird/index.html"
echo.
echo Done.
pause

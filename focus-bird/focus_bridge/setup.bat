@echo off
echo === Focus Bird Pro - Windows Setup ===
echo.
echo Step 1: Check Python 3.11
py -3.11 --version
if %errorlevel% neq 0 (
    echo ERROR: Python 3.11 not found
    echo Download: https://www.python.org/downloads/release/python-3119/
    echo Install it, then run setup.bat again
    pause
    exit /b
)
echo.
echo Step 2: Install pyserial (COM port connection)
py -3.11 -m pip install pyserial
echo.
echo Step 3: Install websockets (optional, only if using --ws mode)
echo To skip, press N. Otherwise press any key.
pause >nul
py -3.11 -m pip install websockets
echo.
echo Step 4: Download BrainLinkParser.pyd
echo URL: https://github.com/Macrotellect/BrainLinkParser-Python
echo Or: https://o.macrotellect.com/index.html#v1
echo.
echo Download BrainLinkParser.pyd and place it in this folder.
echo.
echo === DONE ===
echo.
echo Next steps:
echo  1. Pair BrainLink Pro via Windows Bluetooth
echo     (choose the one with headphone icon)
echo  2. Run: brainlink_pro.py --scan       (find COM port)
echo  3. Run: brainlink_pro.py --port COM5  (connect)
echo.
pause

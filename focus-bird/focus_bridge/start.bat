@echo off
echo === BrainLink Pro EEG Reader ===
echo.
echo Scanning COM ports...
py -3.11 brainlink_pro.py --scan
echo.
echo -------------------------------------------
echo Use the OUTPUT COM port (not INPUT)
echo Check Windows Bluetooth Settings ^> More BT Options ^> COM Ports
echo -------------------------------------------
echo.
set /p PORT=Enter COM port (e.g. COM5): 
echo.
echo Connecting to %PORT%...
echo Press Ctrl+C to stop
echo.
py -3.11 brainlink_pro.py --port %PORT%
echo.
pause

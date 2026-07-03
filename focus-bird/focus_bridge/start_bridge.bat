@echo off
echo === Starting Focus Bird Bridge ===
echo.
echo Available COM ports:
python focus_bridge_windows.py --scan
echo.
set /p PORT=Enter COM port (e.g. COM5): 
python focus_bridge_windows.py --port %PORT% --ws-port 8765
pause

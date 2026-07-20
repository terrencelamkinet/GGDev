@echo off
echo === Starting Focus Bird Bridge ===
echo.
echo Available COM ports:
python brainlink_bridge.py --scan
echo.
echo Starting in AGENT relay mode (via brainlink.kinet-poc.com)
echo.
set /p PORT=Enter COM port (e.g. COM5): 
python brainlink_bridge.py --port %PORT% --config config.txt
pause

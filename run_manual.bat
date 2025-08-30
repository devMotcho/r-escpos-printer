@echo off
REM Run R-ESC/POS Printer manually (not as service)

echo === R-ESC/POS Printer Manual Run ===
echo.
echo Starting the printer application...
echo Press Ctrl+C to stop the application
echo.

REM Change to script directory
cd /d "%~dp0"

REM Run the Python application
python main.py

pause
@echo off
REM Windows Installation Batch File for R-ESC/POS Printer
REM This file runs the PowerShell installation script

echo === R-ESC/POS Printer Installation ===
echo.
echo This script will install all dependencies and setup the service.
echo You need to run this as Administrator!
echo.
pause

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with Administrator privileges...
) else (
    echo ERROR: This script must be run as Administrator!
    echo Right-click this file and select "Run as Administrator"
    pause
    exit /b 1
)

REM Run the PowerShell installation script
echo Starting PowerShell installation script...
powershell -ExecutionPolicy Bypass -File "%~dp0install_windows.ps1"

if %errorLevel% == 0 (
    echo.
    echo Installation completed successfully!
) else (
    echo.
    echo Installation failed with error code %errorLevel%
)

pause
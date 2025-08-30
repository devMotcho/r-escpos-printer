@echo off
REM Launch the Service Management Interface

echo === R-ESC/POS Printer Service Management ===
echo.
echo Opening service management interface...

REM Change to script directory
cd /d "%~dp0"

REM Run the PowerShell service management script
powershell -ExecutionPolicy Bypass -File "%~dp0manage_service.ps1"
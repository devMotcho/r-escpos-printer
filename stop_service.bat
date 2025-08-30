@echo off
REM Stop the R-ESC/POS Printer Service

echo === Stopping R-ESC/POS Printer Service ===
echo.

REM Change to script directory
cd /d "%~dp0"

REM Stop the service using NSSM
nssm.exe stop REscposPrinter

if %errorLevel% == 0 (
    echo Service stopped successfully!
) else (
    echo Failed to stop service. Error code: %errorLevel%
    echo The service may not be running or installed.
)

echo.
pause
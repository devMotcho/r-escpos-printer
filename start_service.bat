@echo off
REM Start the R-ESC/POS Printer Service

echo === Starting R-ESC/POS Printer Service ===
echo.

REM Change to script directory
cd /d "%~dp0"

REM Start the service using NSSM
nssm.exe start REscposPrinter

if %errorLevel% == 0 (
    echo Service started successfully!
) else (
    echo Failed to start service. Error code: %errorLevel%
    echo Check if the service is installed by running install.bat first.
)

echo.
pause
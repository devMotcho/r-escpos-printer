# R-ESC/POS Printer Service Management Script
# This script provides an interactive menu to manage the printer service

$serviceName = "REscposPrinter"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$nssmPath = "$scriptDir\nssm.exe"

function Show-Menu {
    Clear-Host
    Write-Host "=== R-ESC/POS Printer Service Management ===" -ForegroundColor Green
    Write-Host ""
    
    # Check service status
    $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($service) {
        $status = $service.Status
        $color = if ($status -eq "Running") { "Green" } else { "Yellow" }
        Write-Host "Service Status: $status" -ForegroundColor $color
    } else {
        Write-Host "Service Status: Not Installed" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "1. Start Service" -ForegroundColor White
    Write-Host "2. Stop Service" -ForegroundColor White
    Write-Host "3. Restart Service" -ForegroundColor White
    Write-Host "4. View Service Logs" -ForegroundColor White
    Write-Host "5. View Error Logs" -ForegroundColor White
    Write-Host "6. Install/Reinstall Service" -ForegroundColor White
    Write-Host "7. Remove Service" -ForegroundColor White
    Write-Host "8. Run Application Manually" -ForegroundColor White
    Write-Host "9. Exit" -ForegroundColor White
    Write-Host ""
}

function Start-PrinterService {
    Write-Host "Starting service..." -ForegroundColor Yellow
    try {
        & $nssmPath start $serviceName
        Start-Sleep -Seconds 3
        $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
        if ($service -and $service.Status -eq "Running") {
            Write-Host "Service started successfully!" -ForegroundColor Green
        } else {
            Write-Host "Failed to start service. Check logs." -ForegroundColor Red
        }
    } catch {
        Write-Host "Error starting service: $_" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Stop-PrinterService {
    Write-Host "Stopping service..." -ForegroundColor Yellow
    try {
        & $nssmPath stop $serviceName
        Start-Sleep -Seconds 3
        Write-Host "Service stopped successfully!" -ForegroundColor Green
    } catch {
        Write-Host "Error stopping service: $_" -ForegroundColor Red
    }
    Read-Host "Press Enter to continue"
}

function Restart-PrinterService {
    Write-Host "Restarting service..." -ForegroundColor Yellow
    Stop-PrinterService
    Start-Sleep -Seconds 2
    Start-PrinterService
}

function Show-ServiceLogs {
    $logPath = "$scriptDir\logs\service.log"
    if (Test-Path $logPath) {
        Write-Host "=== Service Logs (last 50 lines) ===" -ForegroundColor Cyan
        Get-Content $logPath -Tail 50 | Write-Host
    } else {
        Write-Host "Log file not found at $logPath" -ForegroundColor Yellow
    }
    Read-Host "Press Enter to continue"
}

function Show-ErrorLogs {
    $logPath = "$scriptDir\logs\service-error.log"
    if (Test-Path $logPath) {
        Write-Host "=== Error Logs (last 50 lines) ===" -ForegroundColor Cyan
        Get-Content $logPath -Tail 50 | Write-Host -ForegroundColor Red
    } else {
        Write-Host "Error log file not found at $logPath" -ForegroundColor Yellow
    }
    Read-Host "Press Enter to continue"
}

function Install-PrinterService {
    Write-Host "Installing/Reinstalling service..." -ForegroundColor Yellow
    
    # Stop and remove existing service
    try {
        & $nssmPath stop $serviceName 2>$null
        & $nssmPath remove $serviceName confirm 2>$null
    } catch {
        # Service doesn't exist
    }
    
    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
    if (-not $pythonPath) {
        Write-Host "ERROR: Python not found. Please install Python first." -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    $mainScript = "$scriptDir\main.py"
    if (-not (Test-Path $mainScript)) {
        Write-Host "ERROR: main.py not found at $mainScript" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        return
    }
    
    # Install the service
    & $nssmPath install $serviceName $pythonPath $mainScript
    & $nssmPath set $serviceName DisplayName "R-ESC/POS Printer Service"
    & $nssmPath set $serviceName Description "Automated ESC/POS thermal printer service for order processing"
    & $nssmPath set $serviceName Start SERVICE_AUTO_START
    & $nssmPath set $serviceName AppDirectory $scriptDir
    & $nssmPath set $serviceName AppStdout "$scriptDir\logs\service.log"
    & $nssmPath set $serviceName AppStderr "$scriptDir\logs\service-error.log"
    
    # Create logs directory if it doesn't exist
    $logsDir = "$scriptDir\logs"
    if (-not (Test-Path $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir -Force
    }
    
    Write-Host "Service installed successfully!" -ForegroundColor Green
    Read-Host "Press Enter to continue"
}

function Remove-PrinterService {
    $confirm = Read-Host "Are you sure you want to remove the service? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "Removing service..." -ForegroundColor Yellow
        try {
            & $nssmPath stop $serviceName 2>$null
            & $nssmPath remove $serviceName confirm
            Write-Host "Service removed successfully!" -ForegroundColor Green
        } catch {
            Write-Host "Error removing service: $_" -ForegroundColor Red
        }
    }
    Read-Host "Press Enter to continue"
}

function Run-ApplicationManually {
    Write-Host "Running application manually..." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
        if (-not $pythonPath) {
            Write-Host "ERROR: Python not found. Please install Python first." -ForegroundColor Red
            Read-Host "Press Enter to continue"
            return
        }
        
        Set-Location $scriptDir
        & $pythonPath "main.py"
    } catch {
        Write-Host "Error running application: $_" -ForegroundColor Red
    }
    
    Read-Host "Press Enter to continue"
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Select an option (1-9)"
    
    switch ($choice) {
        "1" { Start-PrinterService }
        "2" { Stop-PrinterService }
        "3" { Restart-PrinterService }
        "4" { Show-ServiceLogs }
        "5" { Show-ErrorLogs }
        "6" { Install-PrinterService }
        "7" { Remove-PrinterService }
        "8" { Run-ApplicationManually }
        "9" { Write-Host "Goodbye!" -ForegroundColor Green }
        default { 
            Write-Host "Invalid option. Please select 1-9." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($choice -ne "9")
# Windows Installation Script for R-ESC/POS Printer
# Run this script as Administrator in PowerShell

param(
    [switch]$SkipPython,
    [switch]$SkipService
)

$ErrorActionPreference = "Stop"

Write-Host "=== R-ESC/POS Printer Windows Installation ===" -ForegroundColor Green
Write-Host "This script will install Python, dependencies, and setup the service." -ForegroundColor Yellow

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = $ScriptDir

Write-Host "Project directory: $ProjectDir" -ForegroundColor Cyan

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Install Python if not present or if not skipped
if (-not $SkipPython) {
    Write-Host "`n=== Checking Python Installation ===" -ForegroundColor Green
    
    if (Test-Command "python") {
        $pythonVersion = python --version
        Write-Host "Found: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "Python not found. Installing Python..." -ForegroundColor Yellow
        
        # Download and install Python
        $pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
        $pythonInstaller = "$env:TEMP\python-installer.exe"
        
        Write-Host "Downloading Python installer..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
        
        Write-Host "Installing Python..." -ForegroundColor Yellow
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Verify installation
        Start-Sleep -Seconds 3
        if (Test-Command "python") {
            $pythonVersion = python --version
            Write-Host "Successfully installed: $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Python installation failed!" -ForegroundColor Red
            exit 1
        }
        
        # Clean up installer
        Remove-Item $pythonInstaller -Force
    }
} else {
    Write-Host "Skipping Python installation check..." -ForegroundColor Yellow
}

# Install pip dependencies
Write-Host "`n=== Installing Python Dependencies ===" -ForegroundColor Green

if (-not (Test-Path "$ProjectDir\requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found in $ProjectDir" -ForegroundColor Red
    exit 1
}

Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip
    python -m pip install -r "$ProjectDir\requirements.txt"
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies: $_" -ForegroundColor Red
    exit 1
}

# Install NSSM (Non-Sucking Service Manager) for service management
Write-Host "`n=== Installing NSSM Service Manager ===" -ForegroundColor Green

$nssmPath = "$ProjectDir\nssm.exe"
if (-not (Test-Path $nssmPath)) {
    Write-Host "Downloading NSSM..." -ForegroundColor Yellow
    $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
    $nssmZip = "$env:TEMP\nssm.zip"
    $nssmExtract = "$env:TEMP\nssm"
    
    Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
    Expand-Archive -Path $nssmZip -DestinationPath $nssmExtract -Force
    
    # Copy the appropriate NSSM executable
    if ([Environment]::Is64BitOperatingSystem) {
        Copy-Item "$nssmExtract\nssm-2.24\win64\nssm.exe" $nssmPath
    } else {
        Copy-Item "$nssmExtract\nssm-2.24\win32\nssm.exe" $nssmPath
    }
    
    # Clean up
    Remove-Item $nssmZip -Force
    Remove-Item $nssmExtract -Recurse -Force
    
    Write-Host "NSSM installed successfully!" -ForegroundColor Green
} else {
    Write-Host "NSSM already exists at $nssmPath" -ForegroundColor Green
}

# Create service configuration
if (-not $SkipService) {
    Write-Host "`n=== Setting up Windows Service ===" -ForegroundColor Green
    
    $serviceName = "REscposPrinter"
    $pythonPath = (Get-Command python).Source
    $mainScript = "$ProjectDir\main.py"
    
    if (-not (Test-Path $mainScript)) {
        Write-Host "ERROR: main.py not found at $mainScript" -ForegroundColor Red
        exit 1
    }
    
    # Stop and remove existing service if it exists
    try {
        & $nssmPath stop $serviceName 2>$null
        & $nssmPath remove $serviceName confirm 2>$null
        Write-Host "Removed existing service" -ForegroundColor Yellow
    } catch {
        # Service doesn't exist, continue
    }
    
    # Install the service
    Write-Host "Installing service: $serviceName" -ForegroundColor Yellow
    & $nssmPath install $serviceName $pythonPath $mainScript
    
    # Configure service
    & $nssmPath set $serviceName DisplayName "R-ESC/POS Printer Service"
    & $nssmPath set $serviceName Description "Automated ESC/POS thermal printer service for order processing"
    & $nssmPath set $serviceName Start SERVICE_AUTO_START
    & $nssmPath set $serviceName AppDirectory $ProjectDir
    & $nssmPath set $serviceName AppStdout "$ProjectDir\logs\service.log"
    & $nssmPath set $serviceName AppStderr "$ProjectDir\logs\service-error.log"
    
    # Create logs directory if it doesn't exist
    $logsDir = "$ProjectDir\logs"
    if (-not (Test-Path $logsDir)) {
        New-Item -ItemType Directory -Path $logsDir -Force
        Write-Host "Created logs directory: $logsDir" -ForegroundColor Cyan
    }
    
    # Start the service
    Write-Host "Starting service..." -ForegroundColor Yellow
    & $nssmPath start $serviceName
    
    # Check service status
    Start-Sleep -Seconds 3
    $serviceStatus = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
    if ($serviceStatus -and $serviceStatus.Status -eq "Running") {
        Write-Host "Service started successfully!" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Service may not have started correctly. Check logs in $logsDir" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "Skipping service setup..." -ForegroundColor Yellow
}

# Create desktop shortcuts
Write-Host "`n=== Creating Desktop Shortcuts ===" -ForegroundColor Green

$WshShell = New-Object -comObject WScript.Shell

# Shortcut to run the application manually
$shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\R-ESC POS Printer.lnk")
$shortcut.TargetPath = (Get-Command python).Source
$shortcut.Arguments = "`"$ProjectDir\main.py`""
$shortcut.WorkingDirectory = $ProjectDir
$shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,138"
$shortcut.Description = "R-ESC/POS Printer Application"
$shortcut.Save()

# Shortcut to service management
$shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\Manage R-ESC Printer Service.lnk")
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$ProjectDir\manage_service.ps1`""
$shortcut.WorkingDirectory = $ProjectDir
$shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,21"
$shortcut.Description = "Manage R-ESC/POS Printer Service"
$shortcut.Save()

Write-Host "Desktop shortcuts created!" -ForegroundColor Green

# Final summary
Write-Host "`n=== Installation Complete ===" -ForegroundColor Green
Write-Host "Project installed at: $ProjectDir" -ForegroundColor Cyan
Write-Host "Service name: REscposPrinter" -ForegroundColor Cyan
Write-Host "Logs directory: $ProjectDir\logs" -ForegroundColor Cyan
Write-Host ""
Write-Host "The service will start automatically when Windows boots." -ForegroundColor Yellow
Write-Host "Use the desktop shortcuts to run manually or manage the service." -ForegroundColor Yellow
Write-Host ""
Write-Host "To manually control the service, use:" -ForegroundColor White
Write-Host "  Start: .\nssm.exe start REscposPrinter" -ForegroundColor Gray
Write-Host "  Stop:  .\nssm.exe stop REscposPrinter" -ForegroundColor Gray
Write-Host "  Remove: .\nssm.exe remove REscposPrinter confirm" -ForegroundColor Gray

Write-Host "`nInstallation completed successfully!" -ForegroundColor Green
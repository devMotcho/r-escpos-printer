# Installation Validation Script for R-ESC/POS Printer
# This script validates that all components are properly installed

$ErrorActionPreference = "Continue"

Write-Host "=== R-ESC/POS Printer Installation Validation ===" -ForegroundColor Green
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$issues = @()
$warnings = @()

# Function to add issue
function Add-Issue($message) {
    $script:issues += $message
    Write-Host "❌ $message" -ForegroundColor Red
}

# Function to add warning
function Add-Warning($message) {
    $script:warnings += $message
    Write-Host "⚠️  $message" -ForegroundColor Yellow
}

# Function to show success
function Show-Success($message) {
    Write-Host "✅ $message" -ForegroundColor Green
}

Write-Host "=== Checking Python Installation ===" -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Show-Success "Python found: $pythonVersion"
    } else {
        Add-Issue "Python not found or not in PATH"
    }
} catch {
    Add-Issue "Python not found or not accessible"
}

# Check pip
try {
    $pipVersion = python -m pip --version 2>$null
    if ($pipVersion) {
        Show-Success "Pip found: $pipVersion"
    } else {
        Add-Issue "Pip not found or not working"
    }
} catch {
    Add-Issue "Pip not accessible"
}

Write-Host "`n=== Checking Project Files ===" -ForegroundColor Cyan

# Check main files
$requiredFiles = @(
    "main.py",
    "requirements.txt",
    "install_windows.ps1",
    "manage_service.ps1"
)

foreach ($file in $requiredFiles) {
    $filePath = Join-Path $scriptDir $file
    if (Test-Path $filePath) {
        Show-Success "Found: $file"
    } else {
        Add-Issue "Missing required file: $file"
    }
}

Write-Host "`n=== Checking Dependencies ===" -ForegroundColor Cyan

if (Test-Path "$scriptDir\requirements.txt") {
    $requirements = Get-Content "$scriptDir\requirements.txt"
    $packagesToCheck = @("pystray", "python-escpos", "requests", "pydantic", "python-dotenv")
    
    foreach ($package in $packagesToCheck) {
        try {
            $result = python -c "import $($package.Replace('-', '_')); print('OK')" 2>$null
            if ($result -eq "OK") {
                Show-Success "Python package installed: $package"
            } else {
                Add-Issue "Python package missing: $package"
            }
        } catch {
            Add-Issue "Error checking package: $package"
        }
    }
} else {
    Add-Issue "requirements.txt not found"
}

Write-Host "`n=== Checking Service Components ===" -ForegroundColor Cyan

# Check NSSM
$nssmPath = "$scriptDir\nssm.exe"
if (Test-Path $nssmPath) {
    Show-Success "NSSM service manager found"
} else {
    Add-Issue "NSSM not found at $nssmPath"
}

# Check service installation
$serviceName = "REscposPrinter"
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
if ($service) {
    Show-Success "Windows service '$serviceName' is installed"
    $status = $service.Status
    if ($status -eq "Running") {
        Show-Success "Service is currently running"
    } else {
        Add-Warning "Service is installed but not running (Status: $status)"
    }
} else {
    Add-Warning "Windows service '$serviceName' is not installed"
}

Write-Host "`n=== Checking Batch Files ===" -ForegroundColor Cyan

$batchFiles = @(
    "install.bat",
    "run_manual.bat",
    "start_service.bat",
    "stop_service.bat",
    "manage_service.bat"
)

foreach ($file in $batchFiles) {
    $filePath = Join-Path $scriptDir $file
    if (Test-Path $filePath) {
        Show-Success "Found: $file"
    } else {
        Add-Warning "Missing batch file: $file"
    }
}

Write-Host "`n=== Checking Logs Directory ===" -ForegroundColor Cyan

$logsDir = "$scriptDir\logs"
if (Test-Path $logsDir) {
    Show-Success "Logs directory exists"
    
    $logFiles = @("service.log", "service-error.log")
    foreach ($logFile in $logFiles) {
        $logPath = Join-Path $logsDir $logFile
        if (Test-Path $logPath) {
            $size = (Get-Item $logPath).Length
            Show-Success "Log file exists: $logFile ($size bytes)"
        } else {
            Add-Warning "Log file not found: $logFile (will be created when service runs)"
        }
    }
} else {
    Add-Warning "Logs directory doesn't exist (will be created automatically)"
}

Write-Host "`n=== Checking Environment Configuration ===" -ForegroundColor Cyan

$envFile = "$scriptDir\.env"
if (Test-Path $envFile) {
    Show-Success "Environment file (.env) found"
    $envContent = Get-Content $envFile -ErrorAction SilentlyContinue
    if ($envContent) {
        Show-Success "Environment file contains configuration"
    } else {
        Add-Warning "Environment file is empty"
    }
} else {
    Add-Warning "Environment file (.env) not found - you may need to create one"
}

Write-Host "`n=== Desktop Shortcuts ===" -ForegroundColor Cyan

$shortcuts = @(
    "$([Environment]::GetFolderPath('Desktop'))\R-ESC POS Printer.lnk",
    "$([Environment]::GetFolderPath('Desktop'))\Manage R-ESC Printer Service.lnk"
)

foreach ($shortcut in $shortcuts) {
    if (Test-Path $shortcut) {
        Show-Success "Desktop shortcut exists: $(Split-Path $shortcut -Leaf)"
    } else {
        Add-Warning "Desktop shortcut not found: $(Split-Path $shortcut -Leaf)"
    }
}

# Final summary
Write-Host "`n=== VALIDATION SUMMARY ===" -ForegroundColor White

if ($issues.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "🎉 Perfect! All components are properly installed and configured." -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now:" -ForegroundColor Green
    Write-Host "  • Use the service management interface: manage_service.bat" -ForegroundColor Gray
    Write-Host "  • Start the service: start_service.bat" -ForegroundColor Gray
    Write-Host "  • Run manually: run_manual.bat" -ForegroundColor Gray
} else {
    if ($issues.Count -gt 0) {
        Write-Host "❌ Found $($issues.Count) critical issue(s):" -ForegroundColor Red
        foreach ($issue in $issues) {
            Write-Host "   • $issue" -ForegroundColor Red
        }
        Write-Host ""
        Write-Host "Please run install.bat as Administrator to fix these issues." -ForegroundColor Yellow
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host "⚠️  Found $($warnings.Count) warning(s):" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "   • $warning" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "Warnings may not prevent operation but should be reviewed." -ForegroundColor Gray
    }
}

Write-Host "`nValidation completed!" -ForegroundColor White
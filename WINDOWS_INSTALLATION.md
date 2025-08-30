# Windows Installation Guide

This guide will help you install and configure the R-ESC/POS Printer project on Windows as a background service that starts automatically when the machine boots.

## Quick Installation

### Method 1: Automated Installation (Recommended)

1. **Download or clone** this project to your Windows machine
2. **Right-click** on `install.bat` and select **"Run as Administrator"**
3. **Follow the prompts** - the script will automatically:
   - Install Python 3.11 (if not present)
   - Install all required dependencies
   - Download and configure NSSM (service manager)
   - Create the Windows service
   - Start the service
   - Create desktop shortcuts

### Method 2: Manual PowerShell Installation

1. **Open PowerShell as Administrator**
2. **Navigate** to the project directory
3. **Run**: `.\install_windows.ps1`

## Files Created

After installation, you'll have these files:

### Installation Scripts
- `install_windows.ps1` - Main PowerShell installation script
- `install.bat` - Batch file wrapper for easy installation

### Service Management
- `manage_service.ps1` - Interactive service management interface
- `manage_service.bat` - Launch service management
- `nssm.exe` - Service manager executable (downloaded automatically)

### Quick Controls
- `run_manual.bat` - Run the application manually (not as service)
- `start_service.bat` - Start the printer service
- `stop_service.bat` - Stop the printer service

### Desktop Shortcuts (created automatically)
- `R-ESC POS Printer.lnk` - Run application manually
- `Manage R-ESC Printer Service.lnk` - Open service management interface

## Service Management

### Using the Interactive Interface

Double-click `manage_service.bat` to open an interactive menu where you can:
- Start/Stop/Restart the service
- View service logs
- View error logs
- Install/Reinstall the service
- Remove the service
- Run the application manually

### Using Command Line

```cmd
# Start service
nssm.exe start REscposPrinter

# Stop service
nssm.exe stop REscposPrinter

# Restart service
nssm.exe restart REscposPrinter

# Remove service
nssm.exe remove REscposPrinter confirm
```

### Using Windows Services

1. Press `Win + R`, type `services.msc`
2. Find "R-ESC/POS Printer Service"
3. Right-click for options (Start, Stop, Properties, etc.)

## Service Configuration

The service is configured with:
- **Name**: `REscposPrinter`
- **Display Name**: "R-ESC/POS Printer Service"
- **Startup Type**: Automatic (starts with Windows)
- **Working Directory**: Project folder
- **Logs**: `logs/service.log` and `logs/service-error.log`

## Logs and Troubleshooting

### Log Files
- **Service Output**: `logs/service.log`
- **Service Errors**: `logs/service-error.log`

### Viewing Logs
- Use the service management interface (option 4 and 5)
- Or manually check the files in the `logs/` folder

### Common Issues

1. **Service won't start**
   - Check if Python is installed: `python --version`
   - Check if dependencies are installed
   - Review error logs
   - Try running manually first: `run_manual.bat`

2. **Permission errors**
   - Ensure you ran installation as Administrator
   - Check Windows firewall settings
   - Verify printer network connectivity

3. **Python not found**
   - Reinstall using: `install_windows.ps1 -SkipService`
   - Or manually install Python from python.org

## Environment Configuration

Make sure to configure your `.env` file with proper settings before starting the service:

```env
# Add your API configuration
BASE_URL=your_api_url
# Add printer configuration
PRINTER_IP=your_printer_ip
# Other settings...
```

## Uninstallation

To completely remove the service and installation:

1. **Stop the service**: Run `stop_service.bat`
2. **Remove the service**: Use service management interface (option 7)
3. **Delete the project folder**
4. **Remove desktop shortcuts** (if desired)

## Manual Testing

Before setting up as a service, test the application manually:

1. Open Command Prompt in the project directory
2. Run: `python main.py`
3. Verify it works correctly
4. Press Ctrl+C to stop

## Requirements

- **Windows 7/10/11** (64-bit recommended)
- **Administrator privileges** for installation
- **Network connection** for downloading dependencies
- **Python 3.11+** (installed automatically)

## Support

If you encounter issues:
1. Check the log files in `logs/` folder
2. Try running the application manually first
3. Use the service management interface for diagnostics
4. Ensure your `.env` file is properly configured

---

**Note**: The service will automatically start when Windows boots. Use the service management tools to control this behavior.
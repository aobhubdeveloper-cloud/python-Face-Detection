# Testing Commands for Environment Setup

## VBA Testing Commands

Run these in Access VBA Immediate Window (Ctrl+G):

### Test Complete Environment
```vba
Call TestEnvironmentSetup()
```
Shows detailed status of Python, packages, and AccessImagine

### Test Only AccessImagine
```vba
Call TestAccessImagine()
```
Detailed AccessImagine ActiveX control test

### Debug AccessImagine Detection
```vba
Call DebugAccessImagine()
```
Comprehensive debug test showing all detection methods

### Register AccessImagine ActiveX
```vba
Call RegisterAccessImagine()
```
Register existing AccessImagine installation

### Find AccessImagine Files
```vba
Call FindAccessImagineFiles()
```
List all AccessImagine DLL/OCX files found

### Launch AccessImagine Sample
```vba
Call LaunchAccessImagineSample()
```
Launch AccessImagine Sample application

### Check AccessImagine Sample
```vba
? AccessImagineSampleExists()
```
Check if AccessImagine Sample is installed

### Test Individual Components
```vba
' Test Python installation
? IsPythonInstalled()

' Test Python packages
? ArePackagesInstalled()

' Test AccessImagine
? IsAccessImagineInstalled()

' Test complete validation
? ValidateEnvironment()
```

### Test Database Startup
```vba
Call TestStartup()
```
Tests environment without opening forms

## Command Line Testing

### Test AccessImagine Installation
```cmd
test_accessimagine.bat
```
Comprehensive AccessImagine detection test

### Test Python Environment
```cmd
python scripts\setup_environment.py
```
Validates Python and packages

## Manual AccessImagine Tests

### PowerShell Commands
```powershell
# Check Windows Apps
Get-AppxPackage | Where-Object {$_.Name -like '*AccessImagine*'}

# Check Registry
Get-ItemProperty "HKLM:\SOFTWARE\Classes\AccessImagine.AccessImagine" -ErrorAction SilentlyContinue
```

### Registry Check
```cmd
reg query "HKLM\SOFTWARE\Classes\AccessImagine.AccessImagine" /ve
```

## Expected Results

### ✅ Success Indicators
- Python: ✓ Installed
- Python Packages: ✓ Installed  
- AccessImagine: ✓ Installed
- Overall Status: ✓ READY

### ❌ Failure Indicators
- Python: ✗ Not Found
- Python Packages: ✗ Missing
- AccessImagine: ✗ Not Found
- Overall Status: ✗ FAILED

## Troubleshooting

If AccessImagine test fails:
1. Run `install_accessimagine.bat` as Administrator
2. Check Windows Apps for "AccessImagine"
3. Verify ActiveX control registration
4. Try manual installation from access.bukrek.net
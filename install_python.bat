@echo off
REM Batch script to download and install Python if not present

echo === Python Installation Check ===

REM Check if Python is already installed
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already installed
    python --version
    goto :install_packages
)

echo Python not found. Downloading Python installer...

REM Create temp directory
if not exist "%TEMP%\python_installer" mkdir "%TEMP%\python_installer"
cd /d "%TEMP%\python_installer"

REM Download Python 3.11 installer (64-bit)
echo Downloading Python 3.11.7...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'"

if not exist "python-installer.exe" (
    echo Failed to download Python installer
    pause
    exit /b 1
)

echo Installing Python...
REM Install Python with pip and add to PATH
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

REM Wait for installation to complete
timeout /t 10 /nobreak >nul

REM Refresh environment variables
call refreshenv.cmd >nul 2>&1

:install_packages
echo.
echo === Installing Required Packages ===

REM Run the Python setup script
python "%~dp0setup_environment.py"

if %errorlevel% == 0 (
    echo.
    echo === Setup Complete ===
    echo Environment is ready for Face Photo Utility
) else (
    echo.
    echo === Setup Failed ===
    echo Please check the error messages above
)

pause
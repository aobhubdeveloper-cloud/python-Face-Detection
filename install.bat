@echo off
echo Installing Face Photo Utility...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or later.
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /f /q "*.spec"

REM Update pip and install basic requirements
echo Updating pip and installing basic requirements...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo Failed to update pip and install basic requirements!
    pause
    exit /b 1
)

REM Install requirements
echo Installing dependencies...
python -m pip install --no-cache-dir opencv-python numpy Pillow pyperclip pyinstaller
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

REM Get OpenCV cascade file paths
echo Locating OpenCV cascade files...
python -c "import cv2; import os; print(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))" > cascade_path.txt
set /p CASCADE_PATH=<cascade_path.txt
del cascade_path.txt

REM Build the executable
echo Building application...
python -m PyInstaller --noconfirm ^
    --add-data "%CASCADE_PATH%;cv2/data/haarcascades" ^
    --add-data "%CASCADE_PATH:haarcascade_frontalface_default.xml=haarcascade_eye.xml%;cv2/data/haarcascades" ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import PIL ^
    --hidden-import PIL._tkinter_finder ^
    --name "FacePhotoUtility" ^
    --onefile ^
    --windowed ^
    face-uitlity.py

if errorlevel 1 (
    echo Failed to build application!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo The executable can be found in the dist directory
echo.
echo Testing executable...
if exist "dist\FacePhotoUtility.exe" (
    echo Executable created successfully!
    echo You can find it at: dist\FacePhotoUtility.exe
) else (
    echo Failed to create executable!
)
pause

if errorlevel 1 (
    echo Failed to build application!
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo The executable can be found in the dist directory
echo.
echo Testing executable...
dist\FacePhotoUtility.exe
pause

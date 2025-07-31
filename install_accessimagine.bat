@echo off
REM Batch script to download and install AccessImagine ActiveX control

echo === AccessImagine Installation ===

REM Create temp directory
if not exist "%TEMP%\accessimagine" mkdir "%TEMP%\accessimagine"
cd /d "%TEMP%\accessimagine"

echo Downloading AccessImagine 1.74...
powershell -Command "Invoke-WebRequest -Uri 'https://access.bukrek.net/down/AccessImagine174.exe' -OutFile 'AccessImagine174.exe'"

if not exist "AccessImagine174.exe" (
    echo Failed to download AccessImagine installer
    pause
    exit /b 1
)

echo Installing AccessImagine ActiveX control...
REM Run the installer
AccessImagine174.exe

echo.
echo Installation complete!
echo AccessImagine ActiveX control should now be available in MS Access.

REM Launch AccessImagine Sample if available
echo.
echo Launching AccessImagine Sample...
if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AccessImagine\AccessImagine Sample.lnk" (
    start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AccessImagine\AccessImagine Sample.lnk"
    echo AccessImagine Sample launched successfully!
) else (
    echo AccessImagine Sample not found in Start Menu
)

REM Clean up
cd /d "%TEMP%"
rmdir /s /q "%TEMP%\accessimagine"

pause
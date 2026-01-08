@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   SRT to Markdown GUI - Create Release Package            ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

set VERSION=v1.0
set RELEASE_NAME=srt-to-markdown-gui-%VERSION%
set RELEASE_DIR=release\%RELEASE_NAME%
set ZIP_FILE=release\%RELEASE_NAME%-windows.zip

:: Check if release folder exists
if not exist "%RELEASE_DIR%" (
    echo ❌ Release folder not found!
    echo.
    echo Please run build-gui-exe.bat first to create the release package.
    echo.
    pause
    exit /b 1
)

echo 📦 Creating release package...
echo.
echo 📁 Source: %RELEASE_DIR%\
echo 📦 Output: %ZIP_FILE%
echo.

:: Delete old ZIP if exists
if exist "%ZIP_FILE%" (
    echo 🗑️  Removing old ZIP file...
    del /q "%ZIP_FILE%"
)

:: Create ZIP using PowerShell
echo 🔨 Compressing files...
powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"

if errorlevel 1 (
    echo.
    echo ❌ Failed to create ZIP file!
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                  RELEASE PACKAGE READY!                    ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo ✅ ZIP file created: %ZIP_FILE%
echo.

:: Get file size
for %%A in ("%ZIP_FILE%") do set SIZE=%%~zA
set /a SIZE_MB=%SIZE% / 1048576
echo 📊 File size: %SIZE_MB% MB
echo.

echo 📁 Package contents:
echo    - SRT-Converter-GUI.exe (Standalone executable)
echo    - README.md (Complete GUI guide)
echo    - QUICK_START.txt (Quick start instructions)
echo    - LICENSE (MIT License)
echo    - examples\ (Sample folder structures)
echo.

echo 🎯 Next steps:
echo    1. Test the package by extracting and running the .exe
echo    2. Upload to GitHub Releases
echo    3. Share with users!
echo.

echo 📤 GitHub Release Notes Template:
echo ═══════════════════════════════════════════════════════════
echo.
echo ## SRT to Markdown Converter - GUI Version %VERSION%
echo.
echo ### 🎨 What's New
echo - Modern GUI interface using CustomTkinter
echo - Dark/Light mode toggle
echo - Real-time progress tracking
echo - User-friendly folder browser
echo - Activity log with status updates
echo.
echo ### 📦 Download
echo - **Windows:** srt-to-markdown-gui-%VERSION%-windows.zip
echo.
echo ### 🚀 Quick Start
echo 1. Extract the ZIP file
echo 2. Double-click `SRT-Converter-GUI.exe`
echo 3. Select mode (Course/YouTube)
echo 4. Browse input folder
echo 5. Click Convert!
echo.
echo ### 📚 Documentation
echo - See `README.md` for complete guide
echo - See `QUICK_START.txt` for quick instructions
echo.
echo ═══════════════════════════════════════════════════════════
echo.

pause

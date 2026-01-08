@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     SRT to Markdown Converter - Build GUI Executable      ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ⚠️  PyInstaller not installed!
    echo.
    echo Installing PyInstaller...
    pip install pyinstaller
    echo.
)

echo 🔨 Building GUI executable...
echo.

:: Build the executable
python -m PyInstaller --onefile --windowed --name "SRT-Converter-GUI" --clean srt_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                    BUILD COMPLETE!                         ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo ✅ Executable created: dist\SRT-Converter-GUI.exe
echo.
echo 📁 Location: %CD%\dist\
echo.
echo 🎯 Next steps:
echo    1. Test the executable: dist\SRT-Converter-GUI.exe
echo    2. Distribute to users
echo.

pause

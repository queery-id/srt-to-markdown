@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     Building SRT to Markdown Converter v3.0              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ⚠️  PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

echo 📦 Building executable...
echo.

:: Build the executable
pyinstaller --onefile ^
    --console ^
    --name "srt-to-markdown" ^
    --icon=NONE ^
    --add-data "README.md;." ^
    srt_to_markdown.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════
echo ✅ Build complete!
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Executable location: dist\srt-to-markdown.exe
echo 📊 File size: 
dir dist\srt-to-markdown.exe | find "srt-to-markdown.exe"
echo.
echo 🧪 Testing executable...
echo.

:: Test the executable
dist\srt-to-markdown.exe --help

if errorlevel 1 (
    echo.
    echo ⚠️  Executable test failed!
) else (
    echo.
    echo ✅ Executable test passed!
)

echo.
echo ═══════════════════════════════════════════════════════════
echo 📦 Next steps:
echo ═══════════════════════════════════════════════════════════
echo  1. Test: dist\srt-to-markdown.exe --youtube
echo  2. Copy to desired location
echo  3. Share with others (no Python needed!)
echo ═══════════════════════════════════════════════════════════
echo.
pause

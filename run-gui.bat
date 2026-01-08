@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     SRT to Markdown Converter - GUI Mode                  ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if customtkinter is installed
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo ⚠️  CustomTkinter not installed!
    echo.
    echo Installing required packages...
    pip install -r requirements-gui.txt
    echo.
)

echo 🚀 Starting GUI...
echo.

python srt_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Error running GUI
    pause
) else (
    echo.
    echo ✅ GUI closed successfully
)

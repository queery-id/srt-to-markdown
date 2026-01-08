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

:: Check if CustomTkinter is installed
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo ⚠️  CustomTkinter not installed!
    echo.
    echo Installing dependencies...
    pip install -r requirements-gui.txt
    echo.
)

echo 🔨 Building GUI executable...
echo.

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist\SRT-Converter-GUI.exe del /q dist\SRT-Converter-GUI.exe

:: Build the executable
python -m PyInstaller --onefile --windowed --name "SRT-Converter-GUI" --clean srt_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Executable built successfully!
echo.

:: Create release folder
echo 📦 Creating release package...
echo.

set RELEASE_DIR=release\srt-to-markdown-gui-v1.0
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%\examples"

:: Copy executable
copy dist\SRT-Converter-GUI.exe "%RELEASE_DIR%\" >nul

:: Copy documentation
copy GUI_GUIDE.md "%RELEASE_DIR%\README.md" >nul
copy QUICK_START_GUI.md "%RELEASE_DIR%\QUICK_START.txt" >nul
copy LICENSE "%RELEASE_DIR%\" >nul

:: Copy examples
xcopy /E /I /Q Input\* "%RELEASE_DIR%\examples\" >nul

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                    BUILD COMPLETE!                         ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo ✅ Executable: dist\SRT-Converter-GUI.exe
echo 📦 Release package: %RELEASE_DIR%\
echo.
echo 📁 Package contents:
echo    - SRT-Converter-GUI.exe
echo    - README.md (GUI Guide)
echo    - QUICK_START.txt
echo    - LICENSE
echo    - examples\ (sample files)
echo.
echo 🎯 Next steps:
echo    1. Test: %RELEASE_DIR%\SRT-Converter-GUI.exe
echo    2. Create ZIP for distribution
echo    3. Upload to GitHub Releases
echo.

pause

@echo off
echo ╔═══════════════════════════════════════════════════════════╗
echo ║     Creating Release Package v3.0                         ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check if dist folder exists
if not exist "dist\srt-to-markdown.exe" (
    echo ❌ Executable not found!
    echo    Please run build-exe.bat first.
    echo.
    pause
    exit /b 1
)

:: Create release folder
set "RELEASE_FOLDER=release\srt-to-markdown-v3.0"
if exist "release" rmdir /s /q "release"
mkdir "%RELEASE_FOLDER%"

echo 📦 Packaging files...
echo.

:: Copy executable
copy "dist\srt-to-markdown.exe" "%RELEASE_FOLDER%\" >nul
echo ✅ Copied: srt-to-markdown.exe

:: Copy documentation
copy "README.md" "%RELEASE_FOLDER%\" >nul
echo ✅ Copied: README.md

copy "TESTING_GUIDE.md" "%RELEASE_FOLDER%\" >nul
echo ✅ Copied: TESTING_GUIDE.md

:: Create quick start guide
echo Creating QUICK_START.txt...
(
echo ═══════════════════════════════════════════════════════════
echo  SRT to Markdown Converter v3.0 - Quick Start
echo ═══════════════════════════════════════════════════════════
echo.
echo 🚀 QUICK START:
echo.
echo 1. COURSE MODE ^(Udemy, Coursera, LinkedIn Learning^):
echo    srt-to-markdown.exe -i "C:\Path\To\Courses"
echo.
echo 2. YOUTUBE MODE ^(Video Collections^):
echo    srt-to-markdown.exe --youtube -i "C:\Path\To\Videos"
echo.
echo 3. INTERACTIVE MODE:
echo    srt-to-markdown.exe --youtube
echo    ^(Script will prompt for folder path^)
echo.
echo ═══════════════════════════════════════════════════════════
echo 📚 EXAMPLES:
echo ═══════════════════════════════════════════════════════════
echo.
echo Course Mode - All courses:
echo   srt-to-markdown.exe
echo.
echo Course Mode - Custom input:
echo   srt-to-markdown.exe -i "D:\MyCourses"
echo.
echo Course Mode - Single course:
echo   srt-to-markdown.exe -c "SQL Bootcamp"
echo.
echo YouTube Mode - Interactive:
echo   srt-to-markdown.exe --youtube
echo.
echo YouTube Mode - Direct:
echo   srt-to-markdown.exe --youtube -i "D:\YouTube\Claude Code"
echo.
echo ═══════════════════════════════════════════════════════════
echo 📁 FOLDER STRUCTURE:
echo ═══════════════════════════════════════════════════════════
echo.
echo Course Mode Input:
echo   Courses/
echo   ├── Course 1/
echo   │   ├── Section 1/
echo   │   │   └── Lecture.srt
echo   │   └── Section 2/
echo   └── Course 2/
echo.
echo YouTube Mode Input:
echo   Topic Folder/
echo   ├── video1.srt
echo   ├── video2.txt
echo   └── video3.srt
echo.
echo Output:
echo   - Course Mode: output/CourseName.md
echo   - YouTube Mode: TopicFolder/TopicName.md ^(same folder^)
echo.
echo ═══════════════════════════════════════════════════════════
echo 💡 TIPS:
echo ═══════════════════════════════════════════════════════════
echo.
echo - Supports .srt and .txt subtitle files
echo - No Python installation required
echo - Works on Windows 10/11
echo - Output format: Markdown ^(.md^)
echo - Perfect for NotebookLM, Custom GPT, Obsidian
echo.
echo ═══════════════════════════════════════════════════════════
echo 📖 FULL DOCUMENTATION:
echo ═══════════════════════════════════════════════════════════
echo.
echo See README.md for complete documentation
echo See TESTING_GUIDE.md for testing examples
echo.
echo GitHub: https://github.com/queery-id/srt-to-markdown
echo.
echo ═══════════════════════════════════════════════════════════
) > "%RELEASE_FOLDER%\QUICK_START.txt"
echo ✅ Created: QUICK_START.txt

:: Create example folders
mkdir "%RELEASE_FOLDER%\examples\course-mode" >nul 2>&1
mkdir "%RELEASE_FOLDER%\examples\youtube-mode" >nul 2>&1

echo.
echo 📝 Creating example README...
(
echo # Examples
echo.
echo ## Course Mode Example
echo.
echo Place your course folders in `course-mode/` folder:
echo.
echo ```
echo course-mode/
echo └── SQL Bootcamp/
echo     ├── Section 1/
echo     │   ├── 1. Introduction.srt
echo     │   └── 2. Setup.srt
echo     └── Section 2/
echo         └── 1. Queries.srt
echo ```
echo.
echo Then run:
echo ```
echo srt-to-markdown.exe -i "examples\course-mode"
echo ```
echo.
echo ## YouTube Mode Example
echo.
echo Place your video subtitles in `youtube-mode/` folder:
echo.
echo ```
echo youtube-mode/
echo └── Claude Code/
echo     ├── video1.srt
echo     ├── video2.txt
echo     └── video3.srt
echo ```
echo.
echo Then run:
echo ```
echo srt-to-markdown.exe --youtube -i "examples\youtube-mode\Claude Code"
echo ```
) > "%RELEASE_FOLDER%\examples\README.md"
echo ✅ Created: examples\README.md

echo.
echo ═══════════════════════════════════════════════════════════
echo ✅ Package created successfully!
echo ═══════════════════════════════════════════════════════════
echo.
echo 📁 Location: %RELEASE_FOLDER%\
echo.
echo 📦 Contents:
dir /b "%RELEASE_FOLDER%"
echo.
echo 💾 Creating ZIP archive...
echo.

:: Create ZIP using PowerShell
powershell -Command "Compress-Archive -Path '%RELEASE_FOLDER%\*' -DestinationPath 'release\srt-to-markdown-v3.0-windows.zip' -Force"

if exist "release\srt-to-markdown-v3.0-windows.zip" (
    echo ✅ ZIP created: release\srt-to-markdown-v3.0-windows.zip
    echo.
    echo 📊 Archive size:
    dir "release\srt-to-markdown-v3.0-windows.zip" | find ".zip"
) else (
    echo ⚠️  ZIP creation failed
)

echo.
echo ═══════════════════════════════════════════════════════════
echo 🎉 Release package ready!
echo ═══════════════════════════════════════════════════════════
echo.
echo 📤 Ready to distribute:
echo    - Folder: release\srt-to-markdown-v3.0\
echo    - ZIP:    release\srt-to-markdown-v3.0-windows.zip
echo.
echo 🚀 Next steps:
echo    1. Test the executable
echo    2. Upload to GitHub Releases
echo    3. Share with users!
echo.
pause

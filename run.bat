@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ============================================
:: SRT to Markdown Converter - Runner v3.0
:: ============================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║       SRT to Markdown Converter v3.0                      ║
echo ║       Course Mode + YouTube Mode                          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Default paths
set "DEFAULT_INPUT=C:\Users\HYPE\Downloads\Udeler"
set "DEFAULT_OUTPUT=%~dp0output"

:menu
:: Main Menu
echo  Choose a mode:
echo.
echo  ═══════════════════════════════════════════════════════════
echo  📚 COURSE MODE (Udemy, Coursera, LinkedIn Learning)
echo  ═══════════════════════════════════════════════════════════
echo  [1] Process ALL courses (default folders)
echo  [2] Custom INPUT folder
echo  [3] Custom OUTPUT folder  
echo  [4] Custom INPUT and OUTPUT folders
echo  [5] Process SINGLE course
echo.
echo  ═══════════════════════════════════════════════════════════
echo  🎥 YOUTUBE MODE (Video Collections → Knowledge Base)
echo  ═══════════════════════════════════════════════════════════
echo  [6] Process YouTube collection (interactive)
echo  [7] Process YouTube collection (specify folder)
echo.
echo  ═══════════════════════════════════════════════════════════
echo  [8] Exit
echo  ═══════════════════════════════════════════════════════════
echo.

set /p choice="  Enter choice (1-8): "

if "%choice%"=="1" goto run_default
if "%choice%"=="2" goto custom_input
if "%choice%"=="3" goto custom_output
if "%choice%"=="4" goto custom_both
if "%choice%"=="5" goto single_course
if "%choice%"=="6" goto youtube_interactive
if "%choice%"=="7" goto youtube_custom
if "%choice%"=="8" goto end

echo.
echo  ❌ Invalid choice. Please try again.
echo.
timeout /t 2 >nul
cls
goto menu

:: ============================================
:: COURSE MODE OPTIONS
:: ============================================

:run_default
echo.
echo  📚 COURSE MODE - Default Folders
echo  ═══════════════════════════════════════════════════════════
echo    Input:  %DEFAULT_INPUT%
echo    Output: %DEFAULT_OUTPUT%
echo  ═══════════════════════════════════════════════════════════
echo.
python "%~dp0srt_to_markdown.py"
goto done

:custom_input
echo.
echo  📚 COURSE MODE - Custom Input
echo  ═══════════════════════════════════════════════════════════
echo  Current default input: %DEFAULT_INPUT%
set /p INPUT_FOLDER="  Enter custom INPUT folder path: "
if "%INPUT_FOLDER%"=="" set "INPUT_FOLDER=%DEFAULT_INPUT%"
echo.
python "%~dp0srt_to_markdown.py" -i "%INPUT_FOLDER%"
goto done

:custom_output
echo.
echo  📚 COURSE MODE - Custom Output
echo  ═══════════════════════════════════════════════════════════
echo  Current default output: %DEFAULT_OUTPUT%
set /p OUTPUT_FOLDER="  Enter custom OUTPUT folder path: "
if "%OUTPUT_FOLDER%"=="" set "OUTPUT_FOLDER=%DEFAULT_OUTPUT%"
echo.
python "%~dp0srt_to_markdown.py" -o "%OUTPUT_FOLDER%"
goto done

:custom_both
echo.
echo  📚 COURSE MODE - Custom Input and Output
echo  ═══════════════════════════════════════════════════════════
echo  Default input:  %DEFAULT_INPUT%
echo  Default output: %DEFAULT_OUTPUT%
echo.
set /p INPUT_FOLDER="  Enter custom INPUT folder path (or press Enter for default): "
set /p OUTPUT_FOLDER="  Enter custom OUTPUT folder path (or press Enter for default): "
if "%INPUT_FOLDER%"=="" set "INPUT_FOLDER=%DEFAULT_INPUT%"
if "%OUTPUT_FOLDER%"=="" set "OUTPUT_FOLDER=%DEFAULT_OUTPUT%"
echo.
python "%~dp0srt_to_markdown.py" -i "%INPUT_FOLDER%" -o "%OUTPUT_FOLDER%"
goto done

:single_course
echo.
echo  📚 COURSE MODE - Single Course
echo  ═══════════════════════════════════════════════════════════
set /p COURSE_NAME="  Enter course name (partial match): "
if "%COURSE_NAME%"=="" (
    echo  ❌ No course name entered. Cancelled.
    goto done
)
echo.
python "%~dp0srt_to_markdown.py" -c "%COURSE_NAME%"
goto done

:: ============================================
:: YOUTUBE MODE OPTIONS
:: ============================================

:youtube_interactive
echo.
echo  🎥 YOUTUBE MODE - Interactive
echo  ═══════════════════════════════════════════════════════════
echo  The script will prompt you for the input folder.
echo  Output will be saved in the same folder as input.
echo  ═══════════════════════════════════════════════════════════
echo.
python "%~dp0srt_to_markdown.py" --youtube
goto done

:youtube_custom
echo.
echo  🎥 YOUTUBE MODE - Specify Folder
echo  ═══════════════════════════════════════════════════════════
echo  Enter the folder containing YouTube subtitle files (.srt or .txt)
echo  Output will be saved in the same folder as input.
echo.
set /p YOUTUBE_FOLDER="  Enter YouTube collection folder path: "
if "%YOUTUBE_FOLDER%"=="" (
    echo  ❌ No folder path entered. Cancelled.
    goto done
)
echo.
python "%~dp0srt_to_markdown.py" --youtube -i "%YOUTUBE_FOLDER%"
goto done

:: ============================================
:: COMPLETION
:: ============================================

:done
echo.
echo ════════════════════════════════════════════════════════════
echo  ✅ Process completed! 
echo ════════════════════════════════════════════════════════════
echo.
echo  Would you like to:
echo  [1] Run another task
echo  [2] Exit
echo.
set /p again="  Enter choice (1-2): "
if "%again%"=="1" (
    cls
    goto menu
)
goto end

:end
echo.
echo  👋 Thank you for using SRT to Markdown Converter!
echo.
pause

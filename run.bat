@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ============================================
:: SRT to Markdown Converter - Runner
:: ============================================

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║       SRT to Markdown Converter for NotebookLM v2.0       ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Default paths
set "DEFAULT_INPUT=C:\Users\HYPE\Downloads\Udeler"
set "DEFAULT_OUTPUT=%~dp0output"

:: Menu
echo  Choose an option:
echo.
echo  [1] Process ALL courses (default folders)
echo  [2] Custom INPUT folder
echo  [3] Custom OUTPUT folder  
echo  [4] Custom INPUT and OUTPUT folders
echo  [5] Process SINGLE course
echo  [6] Exit
echo.

set /p choice="  Enter choice (1-6): "

if "%choice%"=="1" goto run_default
if "%choice%"=="2" goto custom_input
if "%choice%"=="3" goto custom_output
if "%choice%"=="4" goto custom_both
if "%choice%"=="5" goto single_course
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
goto menu

:run_default
echo.
echo  Using default folders:
echo    Input:  %DEFAULT_INPUT%
echo    Output: %DEFAULT_OUTPUT%
echo.
python "%~dp0srt_to_markdown.py"
goto done

:custom_input
echo.
echo  Current default input: %DEFAULT_INPUT%
set /p INPUT_FOLDER="  Enter custom INPUT folder path: "
if "%INPUT_FOLDER%"=="" set "INPUT_FOLDER=%DEFAULT_INPUT%"
echo.
python "%~dp0srt_to_markdown.py" -i "%INPUT_FOLDER%"
goto done

:custom_output
echo.
echo  Current default output: %DEFAULT_OUTPUT%
set /p OUTPUT_FOLDER="  Enter custom OUTPUT folder path: "
if "%OUTPUT_FOLDER%"=="" set "OUTPUT_FOLDER=%DEFAULT_OUTPUT%"
echo.
python "%~dp0srt_to_markdown.py" -o "%OUTPUT_FOLDER%"
goto done

:custom_both
echo.
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
set /p COURSE_NAME="  Enter course name (partial match): "
if "%COURSE_NAME%"=="" (
    echo  No course name entered. Cancelled.
    goto done
)
echo.
python "%~dp0srt_to_markdown.py" -c "%COURSE_NAME%"
goto done

:done
echo.
echo ════════════════════════════════════════════════════════════
echo  Process completed! Check output folder for .md files.
echo ════════════════════════════════════════════════════════════

:end
echo.
pause

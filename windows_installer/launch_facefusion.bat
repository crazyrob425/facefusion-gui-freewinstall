@echo off
REM FaceFusion Launcher Batch Script
REM One-click launcher that handles environment activation and startup

echo ========================================
echo FaceFusion Launcher
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please install Miniconda or Anaconda first
    pause
    exit /b 1
)

REM Check if FaceFusion environment exists
conda env list | findstr "facefusion" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo FaceFusion environment not found. Creating...
    call setup_environment.bat
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create environment
        pause
        exit /b 1
    )
)

echo Activating FaceFusion environment...
call conda activate facefusion

REM Check if activation was successful
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

REM Launch the GUI launcher
echo Starting FaceFusion GUI Launcher...
start pythonw.exe windows_installer\launcher.py

echo.
echo FaceFusion launcher started!
echo You can close this window.
timeout /t 3
exit /b 0

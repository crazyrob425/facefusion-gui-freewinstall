@echo off
REM FaceFusion Environment Setup Script
REM Creates and configures the Python environment with all dependencies

echo ========================================
echo FaceFusion Environment Setup
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if conda is installed
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Conda is not installed or not in PATH
    echo Please run the installer first to install Miniconda
    pause
    exit /b 1
)

REM Read accelerator type from config if it exists
set ACCELERATOR=default
if exist install_config.txt (
    for /f "tokens=2 delims==" %%a in ('findstr "accelerator" install_config.txt') do set ACCELERATOR=%%a
)

echo Selected accelerator: %ACCELERATOR%
echo.

REM Check if environment already exists
conda env list | findstr "facefusion" >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo FaceFusion environment already exists.
    choice /c YN /m "Do you want to recreate it"
    if %ERRORLEVEL% EQU 1 (
        echo Removing existing environment...
        call conda env remove -n facefusion -y
    ) else (
        echo Using existing environment
        exit /b 0
    )
)

echo Creating conda environment...
call conda create -n facefusion python=3.12 -y
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create conda environment
    pause
    exit /b 1
)

echo Activating environment...
call conda activate facefusion
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate environment
    pause
    exit /b 1
)

echo Installing FaceFusion dependencies...
python install.py --onnxruntime %ACCELERATOR% --skip-conda
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Environment setup complete!
echo ========================================
echo.
echo You can now launch FaceFusion using the desktop shortcut
echo or by running launch_facefusion.bat
echo.
pause
exit /b 0

@echo off
echo ========================================
echo RoboEscape: Algorithm Hunters
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo [2/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [3/3] Starting game...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Game crashed or exited with error
    pause
)

deactivate

@echo off
setlocal enabledelayedexpansion

echo Starting the FastAPI application...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.x and try again.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a

:: Check if venv exists
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first.
    pause
    exit /b 1
)

:: Activate venv
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment activation script not found!
    echo Please run install.bat again to recreate the environment.
    pause
    exit /b 1
)

:: Display system information
echo.
echo System Information:
echo Python Version: %PYTHON_VERSION%
echo Virtual Environment: venv
echo.

:: Run the FastAPI application
echo Starting the FastAPI application...
python main.py

:: If the application exits, keep the window open
if errorlevel 1 (
    echo.
    echo ERROR: Application exited with an error.
    pause
) else (
    echo.
    echo Application exited successfully.
    pause
)
@echo off
setlocal enabledelayedexpansion

echo Starting Setup...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.x from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed!
    echo Please install pip and try again.
    pause
    exit /b 1
)

:: Remove existing venv if it exists
if exist "venv" (
    echo Removing existing virtual environment...
    :: Try to deactivate any active venv first
    call venv\Scripts\deactivate.bat 2>nul
    :: Wait a moment for processes to release files
    timeout /t 2 /nobreak >nul
    :: Force remove the directory
    rmdir /s /q venv 2>nul
    if exist "venv" (
        echo ERROR: Could not remove existing virtual environment.
        echo Please close any programs using the virtual environment and try again.
        pause
        exit /b 1
    )
)

:: Create virtual environment
echo Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate venv and install requirements
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)

echo Installing requirements...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found!
)

echo.
echo Installation Finished!
echo You can now start the application with start.bat
pause
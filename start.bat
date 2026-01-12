@echo off
title ASCII2PNG Web Launcher
echo [INFO] Checking environment...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b
)

:: Install dependencies (quietly)
echo [INFO] Checking dependencies...
pip install -r requirements.txt >nul 2>&1

:: Start the app
echo [INFO] Starting Web App...
echo [INFO] Your browser should open automatically.
echo [INFO] Close this window to stop the server.
python web_app.py

pause

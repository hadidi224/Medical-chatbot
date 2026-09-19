@echo off
setlocal
echo ===================================================
echo     Medical Chatbot - Launch (Fixed Version)
echo ===================================================
cd /d "%~dp0"

if not exist "venv" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please let the developer know.
    pause
    exit /b 1
)

echo [INFO] Activating Fixed Environment...
call venv\Scripts\activate

echo [INFO] Starting Chatbot...
python app.py

if %errorlevel% neq 0 (
    echo [ERROR] Application crashed.
)
pause

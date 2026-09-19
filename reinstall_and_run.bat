@echo off
setlocal
echo ===================================================
echo     Medical Chatbot - NUCLEAR OPTION (Reinstall)
echo ===================================================
cd /d "%~dp0"

echo [WARNING] This will DELETE the 'venv' folder and recreate it.
echo This is necessary to fix the 'Access Violation' crash.

set /p "choice=Are you sure? (y/n): "
if /i not "%choice%"=="y" exit /b

echo.
echo 1. Removing old environment...
if exist "venv" (
    rmdir /s /q "venv"
    echo Old venv deleted.
)

echo.
echo 2. Creating NEW environment...
python -m venv venv
if %errorlevel% neq 0 ( 
    echo [ERROR] Failed to create venv. 
    pause
    exit /b 1
)

echo.
echo 3. Installing dependencies (This may take a few minutes)...
call venv\Scripts\activate

python -m pip install --upgrade pip
REM Install llama-cpp-python FIRST with specific flags
python -m pip install llama-cpp-python --prefer-binary --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

REM Install rest
pip install -r requirements.txt

echo.
echo ===================================================
echo Installation Complete.
echo.
echo Starting Chatbot...
python app.py
pause

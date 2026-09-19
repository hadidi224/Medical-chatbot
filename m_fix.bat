@echo off
setlocal EnableDelayedExpansion
echo ===================================================
echo     Medical Chatbot - Fix ^& Run (m_fix.bat)
echo ===================================================

cd /d "%~dp0"

:: 1. Force kill python to try and unlock files
taskkill /F /IM python.exe >nul 2>&1

:: 2. Handle existing venv
if exist "venv" (
    echo [INFO] Found existing venv. Trying to rename it...
    set "rand=!RANDOM!"
    ren "venv" "venv_old_!rand!" 2>nul
    
    if exist "venv" (
        echo [WARNING] Could not rename venv. Trying to delete it instead...
        rmdir /s /q "venv" 2>nul
    )
    
    if exist "venv" (
        echo [ERROR] Could not remove or rename venv. It is still locked.
        echo Please close all Python apps or editors using this folder.
        pause
        exit /b 1
    )
)

:: 3. Create new venv
echo [INFO] Creating new Virtual Environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create venv.
    pause
    exit /b %errorlevel%
)

:: 4. Install Dependencies
echo [INFO] Activating and Installing...
call venv\Scripts\activate
python -m pip install --upgrade pip

echo [INFO] Installing pre-built llama-cpp-python...
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

echo [INFO] Installing other requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed!
    pause
    exit /b %errorlevel%
)

:: 5. Run App
echo [INFO] Starting Application...
python app.py
pause

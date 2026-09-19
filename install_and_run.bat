@echo off
REM Fix for Access Violation Crash
REM This script installs the new stable library (llama-cpp-python),
REM downloads the model if needed, and runs the app.

cd /d "%~dp0"

echo ==========================================
echo 1. Installing new dependencies...
echo ==========================================
echo Checking Python version...
python --version

REM 0. Activate Venv (Crucial if running from venv path)
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] No venv found. Running with global python.
)

REM Upgrade pip
python -m pip install --upgrade pip setuptools wheel

REM 2. Install dependencies (including CTransformers)
echo Installing dependencies...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b %errorlevel%
)

REM 3. Verification
python -c "import ctransformers; print('SUCCESS: ctransformers imported')"
if %errorlevel% neq 0 (
    echo [ERROR] ctransformers failed to import!
    pause
    exit /b 1
)

REM 4. Requirements already installed above.

echo.
echo ==========================================
echo 2. Ensuring Model is downloaded...
echo ==========================================
python src/download_model.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to download model.
    pause
    exit /b %errorlevel%
)

echo.
echo ==========================================
echo 3. Starting Medical Chatbot...
echo ==========================================
python app.py
if %errorlevel% neq 0 (
    echo.
    echo [CRASH DETECTED] Python exited with code: %errorlevel%
    echo This usually means an Access Violation (3221225477 / 0xC0000005)
    echo Try restarting the script or validiting memory usage.
)
pause

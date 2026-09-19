@echo off
setlocal
echo ===================================================
echo     Medical Chatbot - Cleaner Setup & Run
echo ===================================================

cd /d "%~dp0"


IF EXIST "venv" (
    echo [INFO] removing old venv to ensure clean install...
    rmdir /s /q venv
)

echo [INFO] Creating Virtual Environment...
python -m venv venv


echo [INFO] Activating Virtual Environment...
call venv\Scripts\activate

echo [INFO] Environment Check...
python --version
pip --version

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Installing Dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Dependency installation failed!
    pause
    exit /b %errorlevel%
)

echo [INFO] Verifying LangChain...
python -c "import langchain; print('LangChain version:', langchain.__version__)"
if %errorlevel% neq 0 (
    echo [WARNING] Could not verify LangChain. Installation might be corrupted.
)

echo [INFO] Starting Application...
python app.py
if %errorlevel% neq 0 (
    echo [ERROR] Application crashed. See above for details.
    pause
    exit /b %errorlevel%
)

pause

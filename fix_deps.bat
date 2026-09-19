@echo off
cd /d "%~dp0"
echo [INFO] Activating Virtual Environment...
call venv\Scripts\activate

echo [INFO] Uninstalling problematic packages...
pip uninstall -y llama-cpp-python torch numpy

echo [INFO] Installing validated versions...
pip install "numpy<2.0.0"
pip install torch
pip install llama-cpp-python

echo [INFO] Repair Complete.
pause

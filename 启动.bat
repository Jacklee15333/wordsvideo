@echo off
REM ================================================================
REM  Chuti Studio launcher (double-click). Window stays open; close it to quit.
REM ================================================================
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul || (echo [error] Python not found. Install it from https://www.python.org and tick "Add python.exe to PATH". & pause & exit /b 1)
where git >nul 2>nul || (echo [error] Git not found. Install it from https://git-scm.com & pause & exit /b 1)
python -c "import openpyxl" 2>nul || (python -m pip install openpyxl || python -m pip install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple)
python -c "import playwright" 2>nul || (python -m pip install playwright || python -m pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple)
python app\server.py
echo.
echo Stopped. If there is an error above, take a screenshot.
pause

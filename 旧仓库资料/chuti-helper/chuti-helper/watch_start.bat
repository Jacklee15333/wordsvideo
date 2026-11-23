@echo off
cd /d "%~dp0"
start "" pythonw chuti_helper.py watch
echo watch started. log: logs\helper.log
timeout /t 3 >nul

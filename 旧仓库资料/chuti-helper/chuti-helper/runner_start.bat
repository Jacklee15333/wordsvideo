@echo off
cd /d "%~dp0"
start "" /min cmd /c "python runner.py >> logs\runner_console.log 2>&1"

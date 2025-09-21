@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%console.py
set COMMAND_FILE=%SCRIPT_DIR%script2.txt

python "%SCRIPT_PATH%" "C:\home\app" "%COMMAND_FILE%"

pause
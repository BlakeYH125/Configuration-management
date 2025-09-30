@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%console.py
set COMMAND_FILE=%SCRIPT_DIR%multiScript.txt

python "%SCRIPT_PATH%" "multi.zip" "%COMMAND_FILE%"

pause
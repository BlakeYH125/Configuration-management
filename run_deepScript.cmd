@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%console.py
set COMMAND_FILE=%SCRIPT_DIR%deepScript.txt

python "%SCRIPT_PATH%" "deep.zip" "%COMMAND_FILE%"

pause
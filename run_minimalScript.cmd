@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%console.py
set COMMAND_FILE=%SCRIPT_DIR%minimalScript.txt

python "%SCRIPT_PATH%" "minimal.zip" "%COMMAND_FILE%"

pause
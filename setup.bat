@echo off
color 5

title Checking Python Version
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    pause > nul
)

title Installing Requirements
cd /d "%~dp0"
echo Installing Requirements...
python -m pip install -r requirements.txt

cd tools
title Checking for updates
echo Checking for updates...
python update.py
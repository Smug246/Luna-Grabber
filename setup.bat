@echo off
color 5

title Checking Python Version
python --version | findstr "3.11.2"
if %errorlevel%==0 (
    echo Python 3.11.2 is already installed
) else (
    echo Python 3.11.2 is not installed
    echo Please install Python 3.11.2 and it it to your PATH
    exit /b
)

title Installing Requirements
cd /d "%~dp0"
echo Installing Requirements...
python -m pip install -r requirements.txt

cd tools
title Checking for updates
echo Checking for updates...
python update.py
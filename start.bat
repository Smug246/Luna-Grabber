@echo off
color 5

title Checking Python Version
python --version | findstr "3.9."
if %errorlevel%==0 (
    echo Python 3.11.0 or higher is already installed
) else (
    echo Python 3.11.0 or higher is not installed
    echo Please install Python 3.11.0 or higher and add it to your PATH
    timeout /t 5 >nul
    exit
)

:: Check for update
cd tools
title Checking for updates
echo Checking for updates...
python update.py

:: Ensure we are in the directory where the script resides
cd /d "%~dp0"

:: Create a virtual environment named "env"
echo Creating virtual environment...
python -m venv env

:: Activate the virtual environment
call env\Scripts\activate

:: Install the requirements in the virtual environment
title Installing Requirements in the Virtual Environment
echo Installing Requirements in the Virtual Environment...
python -m pip install -r requirements.txt

:: Ensure we are in the directory where the script resides
cd /d "%~dp0"

:: Run the "builder.pyw" script using the Python from the virtual environment
echo Starting builder.pyw...
python builder.pyw

:: Deactivate the virtual environment after all tasks are completed
deactivate
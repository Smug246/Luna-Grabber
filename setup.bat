@echo off
color 5
title Installing Dependencies...

rem Check if Python 3.11 is installed
python --version | findstr "3.11"
if %errorlevel%==0 (
    echo Python 3.11 is already installed
) else (
    echo Python 3.11 is not installed. Downloading...
    curl -L -o python-3.11.exe https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
    echo Installing Python 3.11...
    start /wait python-3.11.exe /quiet InstallAllUsers=1 Include_test=0
    del python-3.11.exe
    echo Python 3.11 has been installed
)

rem Install requirements
echo Installing requirements...
python -m pip install -r requirements.txt

rem Check for updates
cd tools
echo Checking for updates...
python update.py
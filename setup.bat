@echo off
color 5
title Installing Dependencies...

rem Check if Python 3.11.1 is installed
python --version | findstr "3.11.1"
if %errorlevel%==0 (
    echo Python 3.11.1 is already installed
) else (
    echo Python 3.11.1 is not installed. Downloading...
    curl -L -o python-3.11.1.exe https://www.python.org/ftp/python/3.11.0/python-3.11.1-amd64.exe
    echo Installing Python 3.11.1...
    start /wait python-3.11.1.exe /quiet InstallAllUsers=1 Include_test=0
    del python-3.11.1.exe
    echo Python 3.11.1 has been installed
)

rem Install requirements
echo Installing requirements...
python -m pip install -r requirements.txt

rem Check for updates
cd tools
echo Checking for updates...
python update.py
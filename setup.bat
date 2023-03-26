@echo off
color 5
title Installing Dependencies...

:: idk why smug used rem but we use :: for comments

set "python311path=%localappdata%\Programs\Python\Python311"

if not exist "%python311path%" (
    for /f "tokens=1,2 delims= " %%a in ('powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/ -UseBasicParsing | Select-String -Pattern '3.11.[0-9]{1,2}' -AllMatches | Select-Object -ExpandProperty Matches | Select-Object -ExpandProperty Value | Sort-Object -Descending -Unique | Select-Object -First 1"') do (
        set "PYTHON_VERSION=%%a%%b"
    )
    set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe"
    set "PYTHON_EXE=python-installer.exe"
    curl -L -o %PYTHON_EXE% %PYTHON_URL%
    start /wait %PYTHON_EXE% /quiet /passive InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1 Include_doc=0
    del %PYTHON_EXE%
)

python --version
if not %errorlevel% == 0 (
    echo Python is not installed or not added to path. Please install the newest version of python and add it to path!
    pause
    exit /b 1
)

rem Install requirements
echo Installing requirements...
python -m pip install -r requirements.txt

rem Check for updates
cd tools
echo Checking for updates...
python -m update

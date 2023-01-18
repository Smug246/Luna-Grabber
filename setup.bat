@echo off
:: Enhanced by Godfather
cd /d %~dp0
color 5
title Installing requirements...

python --version > python.txt
if %errorlevel% neq 0 (
    echo Python is not installed or not added to path.
    if exist "%localappdata%\Programs\Python\Python310\python.exe" (
        echo Python is installed but not added to path.
    )
    pause
    exit /b
)

set /p python=<python.txt
del python.txt

for /f "tokens=1,2 delims=." %%a in ("%python%") do set version=%%b
if not %version% lss 11 (
    echo Python version is too high. Please install python 3.10.X or lower
    pause
    exit /b
)

python -m pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Pip is not installed or not added to path.
    if exist "%localappdata%\Programs\Python\Python310\Scripts\pip.exe" (
        echo Pip is installed but not added to path.
    )
    pause
    exit /b
)

python -m pip install -r requirements.txt
cls
cd tools
python update.py

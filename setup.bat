@echo off
color 5

title Checking Python Versions
setlocal enabledelayedexpansion
set "python_versions="

REM Loop through all directories in PATH looking for python executables
set "counter=0"
for /f "delims=" %%I in ('where python') do (
    set "python_exe=%%~fI"
    set "python_dir=!python_exe:\python.exe=!"
    set "python_version="
    for /f "delims=" %%A in ('"!python_exe!" --version 2^>^&1') do (
        set "line=%%A"
        for /f "tokens=2 delims= " %%B in ("!line!") do set "python_version=%%B"
    )
    if defined python_version (
        set "ignore=false"
        if "!python_dir!"=="!python_dir:WindowsApps=!" (
            set /a "counter+=1"
            echo !counter!. Found Python version !python_version!: "!python_exe!"
            set "python_versions[!counter!]=!python_version!"
        )
    )
)

REM Prompt user to choose a Python version
echo.
set /p "selected_number=Enter the number of the desired Python version from the list above: "
echo.

REM Check if the selected number is valid
if not defined python_versions[%selected_number%] (
    echo Invalid selection! Exiting...
    pause > nul
    exit /b 1
)
set "selected_version=!python_versions[%selected_number%]!"

REM Append Python version to the .venv folder name
set "venv_name=.venv_!selected_version!"

title Creating Virtual Environment for Python version !selected_version!
echo Creating Virtual Environment for Python version !selected_version!...
python -m venv "!venv_name!"

title Installing Requirements
echo Installing Requirements...
"!venv_name!\Scripts\pip" install --upgrade -r requirements.txt

title Checking for updates
echo Checking for updates...
"!venv_name!\Scripts\python" tools\update.py

if %errorlevel% equ 0 (
    echo Setup Complete!
    title Luna Grabber Builder
    echo Starting the builder...
    "!venv_name!\Scripts\python" builder.pyw
) else (
    title Setup Failed
    echo Setup Failed!
    echo Check the error message above.
    pause > nul
)

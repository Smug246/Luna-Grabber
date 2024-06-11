@echo off
color 5
title Checking Python Versions
setlocal enabledelayedexpansion
set "python_versions="

:: Check if the batch file has administrator rights
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If the above command fails (meaning the batch file is not running as administrator),
:: restart the batch file, this time with administrator privileges
if %errorlevel% NEQ 0 (
	powershell.exe -Command "Start-Process -Verb RunAs -FilePath \"%~f0\""
	exit /b
)

:: Set woring directory to the directory of the batch file
cd /d "%~dp0"

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
			echo !counter!.^) Found Python version !python_version!: "!python_exe!"
			set "python_versions[!counter!]=!python_version!"
			set "python_paths[!counter!]=!python_exe!"
		)
	)
)

REM If no Python installations are found, display a message and exit
if %counter% equ 0 (
	echo No Python installations found in PATH. Please install Python and try again.: https://www.python.org/downloads/
	pause > nul
	exit /b 1
)

REM Prompt user to choose a Python version
echo.
echo If you want to use Nuitka, you need to select a version 3.4.X - 3.11.X
set /p "selected_number=Enter the left number of the desired Python version from the list above: "
echo.

REM Check if the selected number is valid
if not defined python_versions[%selected_number%] (
	echo Invalid selection! Exiting...
	pause > nul
	exit /b 1
)
set "selected_version=!python_versions[%selected_number%]!"
set "selected_python_path=!python_paths[%selected_number%]!"

REM Append Python version to the .venv folder name
set "venv_name=.venv_!selected_version!"

title Creating Virtual Environment for Python version !selected_version!
echo Creating Virtual Environment for Python version !selected_version!...
"!selected_python_path!" -m venv "!venv_name!"

title Installing Requirements
echo Installing Requirements...
"!venv_name!\Scripts\pip" install -r requirements.txt

title Checking for updates
echo Checking for updates...
"!venv_name!\Scripts\python" tools\update.py

if %errorlevel% equ 0 (
	echo Setup Complete!
	title Luna Grabber Builder
	echo Starting the builder...
	"!venv_name!\Scripts\python" builder.py
) else if %errorlevel% equ 1 (
	title Setup Failed
	echo Setup Failed!
	echo Check the error message above.
	pause > nul
) else if %errorlevel% equ 2 (
	timeout /t 3 /nobreak > nul
)

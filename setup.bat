@echo off
color a
set path = %~dp0
cd %path%
python -m pip install -r requirements.txt
python -m builder
pause
exit
::kdot is cool and timmy is fat
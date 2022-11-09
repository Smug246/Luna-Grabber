@echo off
cd /d %~dp0
color 5
python -m pip install -r requirements.txt
python -m builder

@echo off
color 5
python -m pip install -r requirements.txt
cls
cd tools
python update.py
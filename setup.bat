@echo off
color 5
title Installing requirements...
python -m pip install -r requirements.txt
cls
cd tools
python update.py
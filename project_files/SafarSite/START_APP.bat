@echo off
title Starting Civil Core AI
echo Starting Flask Backend...
:: Start the python script in the background
start /b python app.py
echo Waiting for server to initialize...
timeout /t 3
echo Opening Web Interface...
start http://127.0.0.1:5000
exit
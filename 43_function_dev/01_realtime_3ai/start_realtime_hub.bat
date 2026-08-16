@echo off
chcp 65001 > nul
title 3AI Real-Time Pub/Sub Hub Server
echo ==================================================
echo  Starting 3AI Real-Time Hub Server (Port 8000)
echo ==================================================
python -m uvicorn hub_server:app --host 127.0.0.1 --port 8000 --reload
pause

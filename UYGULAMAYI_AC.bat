@echo off
cd /d "%~dp0"
echo Sunucu baslatiliyor...
start "" http://localhost:8000/borsa-analiz.html
python sunucu.py

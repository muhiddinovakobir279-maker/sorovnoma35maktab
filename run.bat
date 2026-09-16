@echo off
chcp 65001 > nul
title Sorovnoma va Natijalar Portali
echo ========================================================
echo   SO'ROVNOMA VA NATIJALAR PORTALI (GOOGLE SHEETS)
echo ========================================================
echo.
echo Server ishga tushirilmoqda...
start http://localhost:5000
python app.py
pause

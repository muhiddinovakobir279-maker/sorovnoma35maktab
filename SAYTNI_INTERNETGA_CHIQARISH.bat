@echo off
chcp 65001 > nul
title Sorovnoma va Natijalar Portali (Cloudflare Tunnel)
cd /d "%~dp0"
echo ========================================================
echo   SO'ROVNOMA VA NATIJALAR PORTALINI INTERNETGA ULASH
echo ========================================================
echo.
python -u server.py
pause

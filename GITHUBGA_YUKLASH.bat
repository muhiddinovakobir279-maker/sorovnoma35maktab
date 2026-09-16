@echo off
chcp 65001 > nul
title GitHub Repozitoriyasiga Yuklash
cd /d "%~dp0"
echo ========================================================
echo   SO'ROVNOMA PORTALINI GITHUB'GA YUKLASH
echo ========================================================
echo.
echo Repozitoriy: https://github.com/muhiddinovakobir279-maker/sorovnoma35maktab.git
echo.
echo Fayllar yuklanmoqda...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   TABRIKLAYMIZ! FAYLLAR GITHUB'GA MUVAFFAQIYATLI YUKLANDI!
    echo ========================================================
) else (
    echo.
    echo [ESLATMA] Agar brauzerda "Sign in to GitHub" oynasi ochilgan bo'lsa,
    echo unda "Authorize" tugmasini bosing va qaytadan ushbu faylni ishga tushiring.
)
echo.
pause

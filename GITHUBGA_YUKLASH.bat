@echo off
chcp 65001 > nul
title GitHub Repozitoriyasiga Yuklash
cd /d "%~dp0"
echo ========================================================
echo   SO'ROVNOMA PORTALINI GITHUB'GA YUKLASH
echo ========================================================
echo.
set /p REPO_URL="GitHub repozitoriy havolasini kiriting (masalan: https://github.com/username/sorovnoma-portal.git): "

if "%REPO_URL%"=="" (
    echo Xatolik: Havola kiritilmadi!
    pause
    exit /b
)

echo.
echo Repozitoriy ulanmoqda...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
echo Fayllar yuklanmoqda (Push)...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   TABRIKLAYMIZ! FAYLLAR GITHUB'GA YUKLANDI!
    echo ========================================================
) else (
    echo.
    echo Yuklashda xatolik yuz berdi. GitHub'ga kirganingizni tekshiring.
)
pause

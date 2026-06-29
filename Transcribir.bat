@echo off
chcp 65001 >nul
title Transcriptor de Audio

if "%~1"=="" (
    echo.
    echo   Arrastra uno o varios archivos de audio sobre este .bat
    echo   Formatos: ogg, mp3, m4a, wav, opus, flac, aac, wma, mp4, mkv, webm
    echo.
    pause
    exit /b
)

set "WHISPER_MODEL=medium"
py -V:3.14 "%~dp0transcribe.py" %*

echo.
pause

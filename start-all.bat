@echo off
title mset-ai-pipeline Launcher
echo Launching mset-ai-pipeline windows...
C:\Python314\python.exe "%~dp0launch_mset.py"
echo.
echo Windows launched. Running confirm sequence in 2s...
timeout /t 2 /nobreak >nul
C:\Python314\python.exe "%~dp0confirm_mset.py"
echo.
echo Done. Go to Orchestrator window.
pause

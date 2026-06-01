@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File ".\scripts\start-backend.ps1"

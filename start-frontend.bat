@echo off
cd /d "%~dp0frontend"
set "PATH=C:\Program Files\nodejs;%PATH%"
call npm.cmd run dev -- --host 127.0.0.1 --port 5173

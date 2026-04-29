@echo off
chcp 65001 >nul
echo ========================================================
echo       Starting Chemo Pharmacy Management System
echo ========================================================

echo.
echo [1/2] Starting Backend Server (FastAPI)...
start "Backend Server (Port 8000)" cmd /k "cd chemo-pharmacy-backend && .\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting Frontend Server...
start "Frontend Server (Port 8080)" cmd /k "cd Projest && ..\chemo-pharmacy-backend\venv\Scripts\python.exe -m http.server 8080"

echo.
echo ========================================================
echo  All servers are spinning up in separate windows!
echo ========================================================
echo.
echo 🌐 Frontend Website : http://127.0.0.1:8080/login.html
echo ⚙️  Backend API      : http://127.0.0.1:8000/docs
echo.
echo Press any key to close this launcher...
pause >nul

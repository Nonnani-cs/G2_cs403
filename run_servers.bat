@echo off
chcp 65001 >nul
echo ========================================================
echo       Setup and Run - Chemo Pharmacy System
echo ========================================================
echo.

:: ---- STEP 1: Check Python ----
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ไม่พบโปรแกรม Python ในเครื่องนี้!
    echo กรุณาดาวน์โหลดและติดตั้ง Python (เวอร์ชัน 3.10+) จาก python.org
    echo *** ติ๊กถูกที่ช่อง "Add Python to PATH" ตอนติดตั้งด้วย ***
    pause
    exit /b
)

cd chemo-pharmacy-backend

:: ---- STEP 2: Recreate venv if broken (copied from another machine) ----
echo [1/4] ตรวจสอบ Virtual Environment...
IF EXIST "venv\Scripts\python.exe" (
    .\venv\Scripts\python.exe --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo [INFO] venv พังเพราะคัดลอกข้ามเครื่อง ลบแล้วสร้างใหม่...
        rmdir /s /q venv
    )
)
IF NOT EXIST "venv\Scripts\python.exe" (
    echo กำลังสร้าง venv ใหม่...
    python -m venv venv
)

:: ---- STEP 3: Install dependencies ----
echo.
echo [2/4] ติดตั้ง/ตรวจสอบไลบรารี (Dependencies)...
.\venv\Scripts\python.exe -m pip install -q -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ติดตั้ง package ไม่สำเร็จ กรุณาตรวจสอบอินเทอร์เน็ต
    pause
    exit /b
)

:: ---- STEP 4: Seed database if missing ----
echo.
echo [3/4] ตรวจสอบฐานข้อมูล...
IF NOT EXIST "chemo_management.db" (
    echo กำลังสร้างฐานข้อมูลและนำข้อมูลเริ่มต้นเข้า...
    .\venv\Scripts\python.exe seed.py
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] สร้างฐานข้อมูลไม่สำเร็จ!
        pause
        exit /b
    )
    echo [OK] ฐานข้อมูลพร้อมใช้งาน
) ELSE (
    echo [OK] พบฐานข้อมูลแล้ว ข้ามขั้นตอนนี้
)

:: ---- STEP 5: Start servers ----
echo.
echo [4/4] เปิดเซิร์ฟเวอร์...
cd ..

:: Backend on 0.0.0.0 so it accepts connections from any source (Live Server, browser, etc.)
start "Backend API (Port 8000)" cmd /k "cd chemo-pharmacy-backend && .\venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Frontend on 0.0.0.0 as well
start "Frontend Web (Port 8080)" cmd /k "cd Projest && ..\chemo-pharmacy-backend\venv\Scripts\python.exe -m http.server 8080 --bind 0.0.0.0"

:: Give servers 2 seconds to start
timeout /t 2 /nobreak >nul

echo.
echo ========================================================
echo  ระบบเปิดสำเร็จ!
echo ========================================================
echo.
echo  เปิดจากเครื่องนี้:
echo    http://127.0.0.1:8080/login.html
echo.
echo  เปิดจากเครื่องอื่นในวงแลน (LAN):
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*192\."') do (
    set LAN_IP=%%a
    setlocal enabledelayedexpansion
    set LAN_IP=!LAN_IP: =!
    echo    http://!LAN_IP!:8080/login.html
    endlocal
)
echo.
echo  API Docs: http://127.0.0.1:8000/docs
echo.
echo  *** อย่าปิดหน้าต่างสีดำ 2 อันที่เด้งขึ้นมา ***
echo.
pause >nul

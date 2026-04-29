@echo off
chcp 65001 >nul
echo ========================================================
echo       Setup and Run - Chemo Pharmacy System
echo ========================================================
echo.

cd chemo-pharmacy-backend

:: Check if global Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] ไม่พบโปรแกรม Python ในเครื่องนี้!
    echo กรุณาดาวน์โหลดและติดตั้ง Python (เวอร์ชัน 3.10+) จากเว็บไซต์ python.org
    echo *** อย่าลืมติ๊กถูกที่ช่อง "Add Python to PATH" ตอนติดตั้งด้วยครับ ***
    pause
    exit /b
)

echo [1/3] ตรวจสอบความพร้อมของระบบ (Virtual Environment)...
:: Check if venv exists and is healthy
IF EXIST "venv\Scripts\python.exe" (
    .\venv\Scripts\python.exe --version >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo [WARNING] พบไฟล์ระบบเก่าที่คัดลอกมาจากเครื่องอื่น ระบบกำลังทำการรีเซ็ตให้ใหม่...
        rmdir /s /q venv
    )
)

IF NOT EXIST "venv\Scripts\python.exe" (
    echo กำลังสร้างสภาพแวดล้อมใหม่สำหรับเครื่องนี้โดยเฉพาะ (Creating venv)...
    python -m venv venv
)

echo.
echo [2/3] กำลังติดตั้ง/ตรวจสอบไลบรารีที่จำเป็น (Installing Dependencies)...
.\venv\Scripts\python.exe -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] เกิดข้อผิดพลาดในการติดตั้งแพ็กเกจ! กรุณาตรวจสอบอินเทอร์เน็ต
    pause
    exit /b
)

echo.
echo [3/3] กำลังตั้งค่าฐานข้อมูล (Checking Database)...
IF NOT EXIST "chemo_management.db" (
    echo กำลังจำลองข้อมูลเริ่มต้นลงฐานข้อมูล (Seeding database...^)
    .\venv\Scripts\python.exe seed.py
)

echo.
echo [4/4] กำลังเปิดเซิร์ฟเวอร์ (Starting Servers)...
cd ..
start "Backend Server (Port 8000)" cmd /k "cd chemo-pharmacy-backend && .\venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"
start "Frontend Server (Port 8080)" cmd /k "cd Projest && ..\chemo-pharmacy-backend\venv\Scripts\python.exe -m http.server 8080"

echo.
echo ========================================================
echo  เปิดระบบสำเร็จ! หน้าต่างเซิร์ฟเวอร์จะถูกแยกออกไป 2 หน้าต่าง
echo ========================================================
echo 🌐 เว็บไซต์ Frontend : http://127.0.0.1:8080/login.html
echo ⚙️  Backend API      : http://127.0.0.1:8000/docs
echo.
echo สามารถปิดหน้าต่างนี้ได้เลย (แต่ห้ามปิดหน้าต่างสีดำ 2 อันที่เด้งขึ้นมาใหม่)
pause >nul

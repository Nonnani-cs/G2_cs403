# รายงานการวิเคราะห์เส้นทางการไหลของข้อมูล (Data Flow Analysis)

เอกสารฉบับนี้สรุปรายละเอียดความสัมพันธ์ของตัวแปร (Variable Connections), ตำแหน่งในโค้ด (Line Numbers), และหน้าที่ของส่วนประกอบต่างๆ ในโปรเจกต์ระบบจัดการสต็อกยาโรงพยาบาล

## 1. การไหลของข้อมูลจาก Python สู่ HTML (Data Injection Flow)

โครงสร้างหลักของระบบใช้สคริปต์ Python ในการสร้างและอัปเดตเนื้อหาในไฟล์ HTML แบบ Static

### A. ข้อมูลต้นทาง (Python Source)
- **ตัวแปร:** `room_temp_drugs` และ `refrigerated_drugs`
- **ไฟล์:** `Projest/replace_drugs_v3.py` (บรรทัดที่ 1 และ 8)
- **บทบาท:** เก็บรายชื่อยาสามัญในรูปแบบ List ของ Python แยกตามประเภทอุณหภูมิที่จัดเก็บ
- **การเชื่อมต่อ:** ถูกประมวลผลผ่านฟังก์ชัน `generate_manage_rows()` และ `generate_receive_rows()` เพื่อเปลี่ยนเป็นโค้ด HTML `<tr>`

### B. จุดรับข้อมูล (HTML Injection Targets)
- **ID เป้าหมาย:** `drug-list-body`
    - **ไฟล์:** `Projest/manage.html` (บรรทัดที่ 373)
    - **การเชื่อมต่อ:** ถูกระบุเป็น Regex Target ใน `replace_drugs_v3.py` (บรรทัดที่ 49) เพื่ออัดข้อมูลตารางยาลงไป
- **ID เป้าหมาย:** `receive-drug-list-body`
    - **ไฟล์:** `Projest/receive.html`
    - **การเชื่อมต่อ:** ถูกระบุเป็น Regex Target ใน `replace_drugs_v3.py` (บรรทัดที่ 83) สำหรับหน้าเบิก-รับยา

---

## 2. การสื่อสารระหว่างหน้าเว็บ (Cross-Page Communication)

ระบบใช้ `localStorage` ของ Browser เป็นตัวกลางในการรับส่งข้อมูลเนื่องจากไม่มี Backend API แบบ Real-time

### A. ข้อมูลคำนวณและใบสั่งยา
- **Storage Key:** `currentDispense`
- **ตำแหน่งเขียนข้อมูล (Write):** `Projest/dispense.html` (บรรทัดที่ 1231)
- **ตำแหน่งอ่านข้อมูล (Read):** `Projest/prescription.html` (บรรทัดที่ 599)
- **บทบาท:** ส่งผ่านข้อมูล JSON ที่ประกอบด้วยรหัสผู้ป่วย (HN), ปริมาณยาที่คำนวณได้, และรหัสยา เพื่อนำไปใช้พิมพ์ฉลากยาในหน้าถัดไป

### B. การจัดการสิทธิ์และเซสชัน (Authentication & RBAC)
- **Storage Key:** `currentUser`
- **ตำแหน่งเขียนข้อมูล:** `Projest/login.html` (ผ่านฟังก์ชัน `handleLogin`)
- **ตำแหน่งอ่านข้อมูล:** ทุกไฟล์ HTML (เช่น `manage.html`, `prescription.html` บรรทัดที่ 584)
- **บทบาท:** ควบคุมการเข้าถึงหน้าเว็บและปลดล็อคฟังก์ชันระดับสูง (เช่น ปุ่มลบข้อมูลยา) ตามบทบาทของผู้ใช้ (Senior vs General Pharmacist)

---

## 3. ตรรกะการควบคุมภายในหน้าจอ (In-Page Control Logic)

### A. ฐานข้อมูลจำลอง (Mock Data Store)
- **ตัวแปร JS:** `masterData`
- **ไฟล์:** `Projest/manage.html` (บรรทัดที่ 462) และ `Projest/receive.html`
- **บทบาท:** เก็บ Object ข้อมูลรายละเอียดของยาแต่ละชนิด (ชื่อทางการค้า, บาร์โค้ด, จำนวนคงเหลือ)
- **การเชื่อมต่อ:** ถูกเข้าถึงโดยฟังก์ชัน `selectDrug` เมื่อมีการคลิกเลือกแถวในตาราง

### B. ตัวควบคุมการเลือกยา (Selection Controller)
- **ฟังก์ชัน:** `selectDrug(row, code)`
- **ไฟล์:** `Projest/manage.html` (บรรทัดที่ 490)
- **บทบาท:** รับรหัสยา (Product Code) จากการคลิกในตาราง เพื่อดึงข้อมูลจาก `masterData` มาอัปเดตลงในหน้าจอรายละเอียด (Input Fields ต่างๆ)
- **การเชื่อมต่อ:** ถูกฝังไว้ใน Event `onclick` ของทุกแถวตารางยาที่ถูกสร้างโดย Python

### C. ระบบคำนวณปริมาณยาส่วนเหลือ (Residual Calculation)
- **ฟังก์ชัน:** `calculateResidual(drugId, doseMg)`
- **ไฟล์:** `Projest/dispense.html` (บรรทัดที่ 510)
- **บทบาท:** คำนวณปริมาณยาที่ต้องการและยาส่วนที่เหลือจาก Volume รวม
- **การเชื่อมต่อ:** ข้อมูลผลลัพธ์จะถูกเก็บลงใน `currentDispense` เพื่อส่งต่อไปยังหน้าจ่ายยา

---

## 4. สรุปภาพรวม Data Pipeline

1. **Python Script** (Data Input) -> **HTML Template** (Injection) -> **Browser LocalStorage** (Session/State)
2. **User Interaction** (Click Table) -> **JavaScript Function** (`selectDrug`) -> **Mock Data** (`masterData`) -> **UI Update**
3. **Calculation Logic** (`dispense.html`) -> **LocalStorage** (`currentDispense`) -> **Dispensing UI** (`prescription.html`)

---
*วิเคราะห์การทำงานของระบบเรียบร้อย พร้อมรับคำสั่งพัฒนาต่อแล้วครับ*

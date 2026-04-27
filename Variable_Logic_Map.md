# แผนผังตรรกะและตัวแปรของระบบ (Comprehensive Variable Logic Map)

เอกสารฉบับนี้อธิบายหน้าที่และความสัมพันธ์ของตัวแปรหลักทั้งหมดในโปรเจกต์ โดยระบุต้นทาง ปลายทาง และตำแหน่งในโค้ดอย่างละเอียด

---

## 1. ตัวแปรในฝั่ง Python (Data Injection Logic)
ตัวแปรเหล่านี้ทำหน้าที่เป็น "ตัวจ่ายข้อมูล" เพื่ออัดเข้าไปในไฟล์ HTML แบบ Static

### 1.1 `room_temp_drugs` และ `refrigerated_drugs`
*   **หน้าที่:** เก็บรายชื่อยาสามัญแยกตามอุณหภูมิการเก็บรักษา
*   **มาจากไหน (Source):** Hardcoded ใน Python List
*   **ไปที่ไหน (Destination):** ถูกแปลงเป็น HTML `<tr>` และอัดลงใน `manage.html` และ `receive.html`
*   **ตำแหน่ง:** `Projest/replace_drugs_v3.py` (บรรทัดที่ 1 และ 8)
*   **ความสัมพันธ์:** เชื่อมต่อกับฟังก์ชัน `generate_manage_rows()` เพื่อสร้างข้อมูลตาราง

### 1.2 `filepath`
*   **หน้าที่:** กำหนดเส้นทางไฟล์ HTML ที่ต้องการแก้ไข
*   **มาจากไหน (Source):** Hardcoded String
*   **ไปที่ไหน (Destination):** ฟังก์ชัน `open()` และ `write()` ของ Python
*   **ตำแหน่ง:** พบในสคริปต์ Python ทุกไฟล์ (บรรทัดที่ 3-5)
*   **ความสัมพันธ์:** เป็นตัวกำหนดว่าสคริปต์นั้นจะส่งผลกระทบกับหน้าจอ (UI) ไหน

### 1.3 `new_rows`
*   **หน้าที่:** เก็บ String ของโค้ด HTML ตารางที่สร้างขึ้นใหม่
*   **มาจากไหน (Source):** ผลลัพธ์จากฟังก์ชัน `generate_manage_rows()`
*   **ไปที่ไหน (Destination):** ถูกนำไปแทนที่ใน `<tbody>` ผ่าน Regex
*   **ตำแหน่ง:** `Projest/replace_drugs_v3.py` (บรรทัดที่ 48 และ 82)

---

## 2. ตัวแปรในฝั่ง JavaScript (State & UI Logic)
ตัวแปรเหล่านี้ทำหน้าที่ควบคุมการแสดงผลและการทำงานบน Browser ของผู้ใช้

### 2.1 `masterData`
*   **หน้าที่:** เก็บข้อมูลรายละเอียดเชิงลึกของยา (ชื่อ, บาร์โค้ด, ราคา, จำนวนคงเหลือ)
*   **มาจากไหน (Source):** ประกาศเป็น Object ว่างใน HTML (และรอรับการ Inject ข้อมูลจาก Python ในอนาคต)
*   **ไปที่ไหน (Destination):** ฟังก์ชัน `selectDrug()` และ `handleScan()`
*   **ตำแหน่ง:** `Projest/manage.html` (บรรทัด 899), `Projest/receive.html` (บรรทัด 518)
*   **ความสัมพันธ์:** เป็นฐานข้อมูลหลัก (Mock DB) ประจำหน้าจอ

### 2.2 `currentDrugCode`
*   **หน้าที่:** เก็บสถานะว่าผู้ใช้กำลังคลิกเลือกดูยาตัวไหนอยู่
*   **มาจากไหน (Source):** ฟังก์ชัน `selectDrug(row, code)`
*   **ไปที่ไหน (Destination):** ใช้ใน `editCurrentDrug()` และ `renderLotTable()`
*   **ตำแหน่ง:** `Projest/manage.html` (บรรทัด 960)

### 2.3 `drugInventory`
*   **หน้าที่:** เก็บค่าคงที่ทางเภสัชกรรม (ปริมาณรวมขวด, ความเข้มข้น) สำหรับคำนวณยา
*   **มาจากไหน (Source):** Hardcoded Object ใน JS
*   **ไปที่ไหน (Destination):** ฟังก์ชัน `calculateResidual()`
*   **ตำแหน่ง:** `Projest/dispense.html` (บรรทัด 473)

### 2.4 `residualStock`
*   **หน้าที่:** เก็บปริมาณยา "เศษ" ที่เหลืออยู่ในตู้เย็นแบบ Real-time (ในหน้านั้นๆ)
*   **มาจากไหน (Source):** Mock Data และผลจากการคำนวณในฟังก์ชัน `goToDispense()`
*   **ไปที่ไหน (Destination):** แสดงผลใน `openResidualModal()`
*   **ตำแหน่ง:** `Projest/dispense.html` (บรรทัด 480)

---

## 3. HTML IDs (DOM Interaction Targets)
IDs เหล่านี้คือ "จุดเชื่อมต่อ" ที่ JavaScript หรือ Python ใช้เข้าถึง Element บนหน้าจอ

### 3.1 `drug-list-body`
*   **หน้าที่:** แสดงรายการยาใน Sidebar ด้านซ้าย
*   **แหล่งข้อมูล:** ถูก Python อัดข้อมูลลงมาที่นี่
*   **ตำแหน่ง:** `Projest/manage.html` (บรรทัด 508)
*   **การเชื่อมต่อ:** JavaScript ฟังก์ชัน `searchDrugs()` จะมาดึง `tr` ในนี้ไปซ่อนหรือแสดง

### 3.2 `order-no` และ `patient-name`
*   **หน้าที่:** รับรหัส HN และชื่อผู้ป่วย
*   **แหล่งข้อมูล:** ผู้ใช้พิมพ์ หรือดึงมาจาก `localStorage`
*   **ตำแหน่ง:** `Projest/dispense.html` (บรรทัด 253 และ 258)
*   **การเชื่อมต่อ:** เชื่อมกับฟังก์ชัน `syncPrescriptionData()` เพื่ออัปเดตข้อมูลแบบ Real-time

### 3.3 `items-table-body`
*   **หน้าที่:** แสดงรายการยาที่อยู่ในใบสั่งยาปัจจุบัน
*   **แหล่งข้อมูล:** ฟังก์ชัน `renderMedTable()`
*   **ตำแหน่ง:** `Projest/dispense.html` (บรรทัด 354)

---

## 4. LocalStorage Keys (Persistence)
ข้อมูลที่ส่งข้ามหน้าเว็บหรือเก็บสถานะการเข้าระบบ

### 4.1 `currentUser`
*   **หน้าที่:** เก็บข้อมูลผู้ใช้ที่ Login อยู่ (ชื่อ, บทบาท)
*   **มาจากไหน (Source):** `login.html` (ฟังก์ชัน `handleLogin`)
*   **ไปที่ไหน (Destination):** ทุกหน้า HTML เพื่อตรวจสอบสิทธิ์ (RBAC)
*   **ความสัมพันธ์:** ใช้ปลดล็อคเมนู `#nav-users` ใน Sidebar

### 4.2 `currentDispense`
*   **หน้าที่:** ส่งข้อมูลผลการคำนวณยาข้ามหน้า
*   **มาจากไหน (Source):** `dispense.html` (ฟังก์ชัน `goToDispense()`)
*   **ไปที่ไหน (Destination):** `prescription.html` (เพื่อนำไปพิมพ์ฉลาก)
*   **รูปแบบข้อมูล:** JSON Object (HN, ชื่อคนไข้, รายการยาที่คำนวณแล้ว)

---

## 5. Database Fields (SQL Structure)
ฟิลด์ข้อมูลใน MySQL ที่ระบบออกแบบมารองรับ (Mapping กับ UI)

*   **`drug_code` (ในตาราง `drugs`):** เชื่อมกับ `PD-ID` ใน UI และตัวแปร `code`
*   **`hn` (ในตาราง `patients`):** เชื่อมกับ ID `hn-input` และ `order-no`
*   **`total_stock`:** เชื่อมกับ `receive-stock-count` ในหน้ารับยา
*   **`is_high_alert`:** เชื่อมกับ Checkbox ในหน้าจัดการยา และปุ่ม `HAD Safety Check`

---
*วิเคราะห์แผนผังตัวแปรและตรรกะเรียบร้อย พร้อมรับคำสั่งพัฒนาต่อตามแผนที่วางไว้ครับ*

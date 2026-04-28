# 📋 Code Analysis & Variable Mapping Report
## ระบบจัดการยาเคมีบำบัดโรงพยาบาล (Chemotherapy Pharmacy Management System)

**Prepared Date:** 28 April 2026  
**Status:** Analysis Complete  
**Role:** Senior Code Analyzer & System Architect

---

## ✅ PART 1: System Flow Explanation (อธิบายการทำงานของระบบ)

### 1.1 System Overview
ระบบจัดการยาเคมีบำบัด (Chemotherapy Pharmacy Management System - CHEMO) เป็นระบบจัดการสต็อกยาและการจ่ายยาเคมีบำบัดโรงพยาบาล ที่ออกแบบให้เภสัชกรสามารถบริหารจัดการยาตั้งแต่การรับเข้า การเก็บบันทึก และการจ่ายยาให้แก่ผู้ป่วยได้อย่างปลอดภัยและมีประสิทธิภาพ

### 1.2 Architecture Flow: Frontend → Backend → Database

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend Layer                      │
│                      (HTML + CSS + JavaScript)              │
├─────────────────────────────────────────────────────────────┤
│  • login.html         - ระบบเข้าสู่ระบบและลงทะเบียน        │
│  • index.html         - หน้าหลัก Dashboard                  │
│  • receive.html       - หน้าเบิก-รับยาเข้าคลัง             │
│  • manage.html        - หน้าจัดการข้อมูลยา               │
│  • dispense.html      - หน้าจัดการใบสั่งยา                │
│  • prescription.html  - หน้าจ่ายยา                       │
│  • patients.html      - หน้าจัดการข้อมูลผู้ป่วย            │
│  • status.html        - หน้าตรวจสอบสถานะยา               │
│  • report.html        - หน้าจัดพิมพ์รายงาน               │
│  • users.html         - หน้าจัดการผู้ใช้ (Admin only)     │
└─────────────────────────────────────────────────────────────┘
                              ↓↑
                      (localStorage)
           ┌──────────────────────────────────────┐
           │    Client-Side Data Storage          │
           │  • currentUser (Session)             │
           │  • chemo_users (User Database)       │
           │  • Mock Data (Temp Storage)          │
           └──────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────┐
│                    Logical Backend Layer                    │
│              (Python Scripts for Maintenance)               │
├─────────────────────────────────────────────────────────────┤
│  • clean_template.py          - ทำความสะอาดข้อมูลจำลอง    │
│  • add_manage_interaction.py   - เพิ่มการโต้ตอบในหน้า manage│
│  • fix_*.py (multiple scripts) - แก้ไข UI/Layout          │
│  • replace_drugs.py            - อัปเดตข้อมูลยา            │
└─────────────────────────────────────────────────────────────┘
                              ↓↑
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer (MySQL)                   │
│                  chemo_management Database                  │
├─────────────────────────────────────────────────────────────┤
│  Tables:                                                    │
│  • users                  - ข้อมูลผู้ใช้ระบบ               │
│  • patients               - ข้อมูลผู้ป่วย                  │
│  • drugs                  - ข้อมูลยา                      │
│  • drug_labels            - ฉลากยาและวิธีใช้             │
│  • drug_lots              - ล็อตและวันหมดอายุ            │
│  • prescriptions          - ใบสั่งยา                     │
│  • prescription_items     - รายการยาในใบสั่ง             │
│  • receive_orders         - บิลเบิก-รับยา               │
│  • receive_order_items    - รายการยาในการรับ             │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 Data Flow per Feature

#### 📥 **Feature 1: User Authentication (การเข้าสู่ระบบ)**
```
[login.html]
    ↓
Input: username, password
    ↓
[localStorage.getItem('chemo_users')] 
    ↓
Validate: username & password match
    ↓
[localStorage.setItem('currentUser', foundUser)]
    ↓
Redirect to [index.html]
    ↓
All pages check: if (!currentUser) → redirect to login
```
- **Storage:** `chemo_users` array in localStorage (mock users)
- **Current User:** Stored in `currentUser` object in localStorage
- **Default User:** admin/123 with role "Senior Pharmacist"

#### 📦 **Feature 2: Drug Stock Management (การจัดการสต็อกยา)**
```
[manage.html] (Frontend - Data display)
    ↓
Display drug information from mock data or future API
    ↓
User can: Add, Edit, Delete, Search drugs
    ↓
Data submitted to Backend (Python/Database)
    ↓
[drugs table] in MySQL (drug_code, generic_name, stock, price)
[drug_lots table] (lot tracking, expiry dates)
[drug_labels table] (usage instructions)
```

#### 📋 **Feature 3: Prescription Management (การจัดการใบสั่งยา)**
```
[prescription.html] (Frontend)
    ↓
Input: ผู้ป่วย HN, ยา, จำนวน, dosage, duration
    ↓
Create prescription record
    ↓
[prescriptions table] + [prescription_items table]
    ↓
Status updates: 'รอจ่ายยา' → 'กำลังจัดยา' → 'จ่ายยาแล้ว'
```

#### 💊 **Feature 4: Drug Dispensing (การจ่ายยา)**
```
[dispense.html] (Frontend)
    ↓
Display pending prescriptions
    ↓
Pharmacist selects lot to dispense
    ↓
System updates: [prescription_items.dispensed_lot_id]
[drugs.total_stock] reduced
    ↓
Log to database with timestamp & pharmacist ID
```

#### 📥 **Feature 5: Receiving & Stock (การเบิก-รับยา)**
```
[receive.html] (Frontend)
    ↓
Create receive order (สั่งยา)
Input: drug_code, quantity, expected_date
    ↓
[receive_orders] + [receive_order_items]
    ↓
Upon receiving: 
  - Mark received_quantity
  - Add new lot to [drug_lots]
  - Update [drugs.total_stock]
```

#### 👥 **Feature 6: Patient Management (จัดการผู้ป่วย)**
```
[patients.html] (Frontend)
    ↓
Display/Edit patient info: HN, Name, Gender, DOB, Allergies
    ↓
[patients table] in MySQL
```

#### 📊 **Feature 7: Reports & Status (รายงานและสถานะ)**
```
[report.html], [status.html] (Frontend)
    ↓
Query data from tables
    ↓
Display: Stock levels, Near-expiry drugs, Prescription status
```

---

## 📊 PART 2: Variable & Data Dictionary (แผนผังตัวแปร)

### 2.1 Database Schema Variables

| ชื่อตัวแปร / Column | Table | ไฟล์ | บรรทัด | คำอธิบาย | ความสัมพันธ์ |
|---|---|---|---|---|---|
| `user_id` | users | chemo_management.sql | 14 | รหัสผู้ใช้ (Primary Key) | Foreign Key อ้างอิงใน prescriptions, receive_orders |
| `username` | users | chemo_management.sql | 15 | ชื่อผู้ใช้ล็อกอิน (UNIQUE) | ใช้ในการยืนยันตัวตนใน login.html |
| `password_hash` | users | chemo_management.sql | 16 | รหัสผ่านแบบ hash | ตรวจสอบในกระบวนการล็อกอิน |
| `full_name` | users | chemo_management.sql | 17 | ชื่อ-นามสกุลเต็ม | แสดงใน index.html, localStorage |
| `role` | users | chemo_management.sql | 18 | บทบาท (Admin/Pharmacist/Staff) | ควบคุม RBAC - เข้าถึง users.html ได้เฉพาะ Senior Pharmacist |
| `hn` | patients | chemo_management.sql | 27 | Hospital Number (Primary Key) | Foreign Key ใน prescriptions, reference ผู้ป่วย |
| `prefix` | patients | chemo_management.sql | 28 | คำนำหน้าชื่อ (นาย/นาง/นางสาว) | ข้อมูลชื่อผู้ป่วย |
| `first_name` | patients | chemo_management.sql | 29 | ชื่อ | ข้อมูลชื่อผู้ป่วย |
| `last_name` | patients | chemo_management.sql | 30 | นามสกุล | ข้อมูลชื่อผู้ป่วย |
| `gender` | patients | chemo_management.sql | 31 | เพศ (ชาย/หญิง/อื่นๆ) | ข้อมูลประชากรศาสตร์ผู้ป่วย |
| `birth_date` | patients | chemo_management.sql | 32 | วันเกิด | คำนวณอายุผู้ป่วย |
| `weight` | patients | chemo_management.sql | 34 | น้ำหนักตัว (kg) | คำนวณ dosage สูตรยาเคมี |
| `allergies` | patients | chemo_management.sql | 36 | ประวัติการแพ้ยา | High Alert - ตรวจสอบก่อนจ่ายยา |
| `drug_code` | drugs | chemo_management.sql | 45 | รหัสยา (Primary Key) | Foreign Key ใน prescription_items, receive_order_items, drug_labels, drug_lots |
| `barcode` | drugs | chemo_management.sql | 46 | บาร์โค้ด (UNIQUE) | ใช้สแกนเพื่อค้นหายา |
| `generic_name` | drugs | chemo_management.sql | 47 | ชื่อสามัญทางยา | ชื่อวิทยาศาสตร์ของยา |
| `trade_name` | drugs | chemo_management.sql | 48 | ชื่อทางการค้า | ชื่อสัญญาการค้า |
| `drug_group` | drugs | chemo_management.sql | 49 | กลุ่มยา | การจำแนกประเภทยา |
| `unit` | drugs | chemo_management.sql | 50 | หน่วยนับ (เม็ด/ขวด/มล.) | ใช้ในการนับสต็อก |
| `cost_price` | drugs | chemo_management.sql | 51 | ต้นทุน | คำนวณกำไร/ขาดทุน |
| `selling_price` | drugs | chemo_management.sql | 52 | ราคาขาย | แสดงต่อผู้ป่วย |
| `max_quantity` | drugs | chemo_management.sql | 53 | จำนวนสูงสุดที่มีได้ | ตั้งค่าคลังสต็อก |
| `min_quantity` | drugs | chemo_management.sql | 54 | จุดสั่งซื้อเมื่อเหลือ | Alert เมื่อสต็อกต่ำ |
| `is_high_alert` | drugs | chemo_management.sql | 55 | เป็น High Alert Drug หรือไม่ | ยาอันตราย - ต้องตรวจสอบสองครั้ง |
| `total_stock` | drugs | chemo_management.sql | 56 | จำนวนคงเหลือปัจจุบัน | อัปเดตเมื่อรับ/จ่าย |
| `lot_id` | drug_lots | chemo_management.sql | 80 | รหัสล็อต (Primary Key) | Foreign Key ใน prescription_items, reference ยาล็อตเฉพาะ |
| `lot_number` | drug_lots | chemo_management.sql | 82 | เลขที่ล็อต | ติดตามเพื่อ Recall/Recall batch |
| `expiry_date` | drug_lots | chemo_management.sql | 83 | วันหมดอายุ | Alert เมื่อเข้าใกล้หมดอายุ |
| `status` | drug_lots | chemo_management.sql | 86 | สถานะล็อต (ปกติ/ใกล้หมดอายุ/หมดอายุ) | Filter ยาหมดอายุ |
| `prescription_no` | prescriptions | chemo_management.sql | 95 | เลขที่ใบสั่ง (Primary Key) | Foreign Key ใน prescription_items, reference ใบสั่ง |
| `dispensed_by` | prescriptions | chemo_management.sql | 101 | ผู้จ่ายยา (Foreign Key → user_id) | เก็บบันทึกว่าใครจ่ายยา |
| `status` | prescriptions | chemo_management.sql | 100 | สถานะใบสั่ง | 'รอจ่ายยา' → 'กำลังจัดยา' → 'จ่ายยาแล้ว' → 'ยกเลิก' |
| `order_no` | receive_orders | chemo_management.sql | 128 | เลขที่บิล/เบิก (Primary Key) | Foreign Key ใน receive_order_items |
| `pharmacist_id` | receive_orders | chemo_management.sql | 131 | เภสัชกรผู้บันทึก (Foreign Key → user_id) | ใครบันทึกการสั่งซื้อ |
| `status` | receive_orders | chemo_management.sql | 134 | สถานะการรับ | 'รอรับ' → 'รับแล้วบางส่วน' → 'รับครบแล้ว' → 'ยกเลิก' |

---

### 2.2 Frontend JavaScript Variables (localStorage & Session)

| ชื่อตัวแปร | ไฟล์ | บรรทัด | ประเภท | คำอธิบาย | ความสัมพันธ์ |
|---|---|---|---|---|---|
| `currentUser` | login.html | 146 | Object (localStorage) | เก็บข้อมูลผู้ใช้ปัจจุบัน: {fullname, username, role} | ตรวจสอบในทุกหน้า (index.html:29, prescription.html:12 เป็นต้น) |
| `chemo_users` | login.html | 131 | Array of Objects (localStorage) | ฐานข้อมูลผู้ใช้ในฝั่ง Client: [{fullname, username, password, role}] | Search ตรวจสอบการล็อกอิน (line 143) |
| `foundUser` | login.html | 143 | Object | ผล search ผู้ใช้ที่เข้ากัน | ย้ายไปยัง currentUser เพื่อสร้าง Session |

---

### 2.3 HTML Form Elements & IDs (UI Variables)

| ID / Class | ไฟล์ | บรรทัด | ประเภท | คำอธิบาย | ความสัมพันธ์ |
|---|---|---|---|---|---|
| `login-form` | login.html | 51 | Form Element | ฟอร์มล็อกอิน | Form submit handler (line 137) → ตรวจสอบ chemo_users |
| `login-username` | login.html | 56 | Input | ช่อง Username | Value ใช้ใน search (line 139) |
| `login-password` | login.html | 63 | Input | ช่อง Password | Value ใช้ใน search (line 140) |
| `register-form` | login.html | 82 | Form Element | ฟอร์มสมัครสมาชิก | Form submit handler (line 154) → เพิ่มผู้ใช้ใหม่ |
| `reg-fullname` | login.html | 85 | Input | ช่อง ชื่อ-นามสกุล | Push ไปยัง chemo_users array |
| `reg-username` | login.html | 89 | Input | ช่อง Username | Validate UNIQUE (line 168) |
| `reg-password` | login.html | 94 | Input | ช่อง Password | Validate ตรงกับ confirm (line 162) |
| `reg-role` | login.html | 103 | Select | เลือกบทบาท | ตั้งค่า role: 'General Pharmacist' หรือ 'Senior Pharmacist' |
| `user-fullname` | index.html | 79 | Span (Display) | แสดง ชื่อผู้ใช้ | ได้จาก currentUser.fullname (line 260) |
| `user-role` | index.html | 81 | Span (Display) | แสดง บทบาท | ได้จาก currentUser.role (line 261) |
| `user-avatar` | index.html | 77 | Img | รูป Avatar | สร้างจาก currentUser.fullname (line 262) |
| `nav-users` | index.html | 71 | Link (Sidebar) | เมนู "จัดการผู้ใช้" | แสดง/ซ่อนตาม RBAC: role === 'Senior Pharmacist' (line 265) |
| `office-sidebar` | index.html | 37 | Div | Sidebar Navigation | Contains: receive.html, manage.html, dispense.html, prescription.html ฯลฯ |
| `stat-card` | index.html | 119-150 | Div (Stats) | แสดงสถิติ Dashboard | ยังใช้ Mock data (ผู้ป่วยวันนี้, ใบสั่งรอ, ยาเศษ, ยาใกล้หมดอายุ) |

---

### 2.4 Python Helper Scripts Variables

| ไฟล์ | บรรทัด | ตัวแปร | คำอธิบาย | ความสัมพันธ์ |
|---|---|---|---|---|
| clean_template.py | 10 | `value="[^"]*"` (regex) | Clear form input values | ทำความสะอาดข้อมูล mock หลังจากการทดสอบ |
| clean_template.py | 14 | `<tbody>` (regex) | Clear table body content | ลบข้อมูลจำลองออกจากตาราง |
| clean_template.py | 18-26 | `masterData`, `historyData`, `mockBills` | Mock data arrays | ตัวแปร Mock ที่ถูกลบ |
| clean_template.py | 44 | `window.onload` (regex) | ลบการเรียก init เก่า | ป้องกัน mock data auto-load |

---

### 2.5 CSS Classes & Styling Variables

| Class Name | ไฟล์ | ประเภท | คำอธิบาย | ความเชื่อมโยง |
|---|---|---|---|---|
| `.active-link` | index.html:18, prescription.html:24 | CSS Class | ทำให้ sidebar link ที่ active ดูเด่น | ใช้เมื่อเข้าหน้านั้นๆ |
| `.stat-card` | index.html:14 | CSS Class | สไตล์การ์ดสถิติ | Hover effect: translateY(-4px), shadow |
| `.quick-link` | index.html:16 | CSS Class | สไตล์ปุ่ม Quick Tools | Hover: background #eff6ff, border-color #bfdbfe |
| `.office-sidebar` | index.html:12 | CSS Class | Sidebar styling | background white, border-right, z-20 |
| `.glass` | login.html:16 | CSS Class | Glass-morphism effect | backdrop-filter: blur(10px) |

---

## 📝 PART 3: Code Quality & Issues Analysis

### 3.1 Dead Code & Unused Variables

| Item | ไฟล์ | สถานะ | หมายเหตุ |
|---|---|---|---|
| `masterData` array | manage.html, dispense.html | ⚠️ Mock Data | ไม่ต่อกับ Backend - ใช้ mock data ชั่วคราว |
| `checkoutList` | prescription.html | ⚠️ Mock Data | ยังไม่มีการเชื่อมต่อกับ DB |
| `mockBills` | receive.html | ⚠️ Mock Data | ยังใช้ข้อมูลจำลอง |
| `btn-settings` button | index.html:220 | ⚠️ Non-functional | Button ยังไม่มีการจัดการ event |
| Python fix_*.py scripts | Projest/ | ✅ Helper Scripts | ใช้สำหรับแก้ไข HTML layout ที่มีอยู่ |

### 3.2 Data Flow Issues (ความสำคัญ)

| ประเด็น | ความรุนแรง | อธิบาย |
|---|---|---|
| Client-side User Storage | 🔴 **Critical** | ใช้ localStorage สำหรับ password - ควรใช้ session server หรือ JWT tokens แทน |
| No Backend API Connection | 🟡 **High** | HTML/JS ยังไม่เชื่อมต่อกับ Backend API - ต้องใช้ AJAX/Fetch จริง |
| Password Plaintext | 🔴 **Critical** | Password เก็บแบบ plaintext ใน localStorage - ต้องใช้ hash + salt |
| No CSRF Protection | 🟡 **High** | Form ไม่มี CSRF token protection |
| Mock Data Hardcoded | 🟡 **Medium** | Mock data hardcoded ใน HTML/JS - ต้องใช้ Backend API |

### 3.3 Positive Notes (จุดแข็ง)

✅ **Schema Design:** Database schema ออกแบบดีมีความชัดเจน (Foreign Keys, Status Enums)  
✅ **RBAC Implementation:** มีการแยกสิทธิ์ผู้ใช้ (Admin/Pharmacist/Staff)  
✅ **UI/UX Design:** Frontend ใช้ Tailwind CSS + Lucide Icons มีดีไซน์สวย  
✅ **Multilingual:** ใช้ภาษาไทยทั้งหมด สะดวกสำหรับผู้ใช้ไทย  
✅ **High Alert Flagging:** ระบบจำหน้าวนิ่งยาอันตราย (is_high_alert)  

---

## 🔗 Data Relationships Summary

```
users ←――┬――→ prescriptions (dispensed_by)
         └――→ receive_orders (pharmacist_id)

patients ←――→ prescriptions (hn)

drugs ←――┬――→ drug_labels (drug_code)
         ├――→ drug_lots (drug_code)
         ├――→ prescription_items (drug_code)
         └――→ receive_order_items (drug_code)

prescriptions ←――→ prescription_items (prescription_no)
receive_orders ←――→ receive_order_items (order_no)

drug_lots ←――→ prescription_items (lot_id - dispensed_lot_id)
```

---

## 📌 Summary

| หัวข้อ | สถานะ | หมายเหตุ |
|---|---|---|
| **Database Schema** | ✅ Complete | 9 tables ครบถ้วน |
| **Frontend Pages** | ✅ Complete | 10 HTML pages |
| **Backend Code** | ⚠️ Not Ready | ต้องเขียน Python/Node.js API |
| **API Integration** | ❌ Missing | ต้องเชื่อมต่อ Frontend ↔ Backend |
| **Authentication** | ⚠️ Mock | ใช้ localStorage ชั่วคราว |
| **CRUD Operations** | ⚠️ Mock | ต้องเขียน API endpoints |
| **Error Handling** | ⚠️ Basic | Alert() ชั่วคราวเท่านั้น |

---

## ✨ Next Steps (ขั้นตอนต่อไป)

1. **เขียน Backend API** (Python Flask/FastAPI หรือ Node.js/Express)
2. **เชื่อมต่อ Frontend ↔ Database** ผ่าน API endpoints
3. **ปรับปรุง Authentication** ใช้ JWT tokens แทน plaintext password
4. **เพิ่ม Error Handling & Validation** ทั้ง Frontend & Backend
5. **ทดสอบการไหลของข้อมูล** (Testing Flow: Login → Create Prescription → Dispense)

---

**วิเคราะห์โค้ดและสร้างแผนผังตัวแปรเรียบร้อยครับ พร้อมรับคำสั่งพัฒนาหรือแก้ไขโค้ดในขั้นตอนต่อไป (หากมีข้อสงสัย ผมจะสอบถามก่อนลงมือทำเสมอ)**

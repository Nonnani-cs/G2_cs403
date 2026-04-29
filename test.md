# 📊 **การวิเคราะห์ระบบจัดการยาเคมีบำบัด**

## **PART 1: SYSTEM FLOW EXPLANATION (การทำงานของระบบ)**

### **1️⃣ Architecture Overview**

ระบบนี้เป็น **Frontend + Backend** ที่ยังอยู่ในสถานะ **Hybrid (Frontend-Heavy)**:
- **Frontend:** HTML/CSS/JavaScript ใช้ localStorage + API calls
- **Backend:** FastAPI Server (Port 8000) ที่เชื่อมต่อ SQLite Database
- **Database:** SQLite (.db file)

---

### **2️⃣ Main Flow ของระบบ**

```
┌─────────────────────────────────────────────────────────────┐
│  1. LOGIN (login.html)                                      │
│  ├─ User enters: username + password                        │
│  ├─ Frontend (JS) → POST /api/auth/login                   │
│  ├─ Backend validates → Return JWT token                   │
│  └─ Save token + currentUser → localStorage                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│  2. DASHBOARD (index.html)                                  │
│  ├─ Display stats: ผู้ป่วยวันนี้, ใบสั่งรอ, ยาเศษ         │
│  ├─ Navigation menu to other pages                         │
│  └─ RBAC: Role-based access (Senior vs General Pharmacist) │
└─────────────────────────────────────────────────────────────┘
                    ↙ ↓ ↘
┌──────────────────┴──┴──────────────────────────────┐
│ 3. MAIN FEATURES (3 major workflows)               │
└──────────────────┬──┬──────────────────────────────┘
        ↙          ↓          ↘
   ┌────────────────────────────────────────────┐
   │ A. MANAGE.HTML (จัดการข้อมูลยา)            │
   ├─────────────────────────────────────────────┤
   │ ✓ Display: Master drug list (10 cancer drugs)  │
   │ ✓ Select drug → Show details (tabs):         │
   │   - Tab 1: General info + labels (TH/EN)    │
   │   - Tab 2: Lot details                      │
   │   - Tab 3: Expiry tracking                  │
   │ ✓ Functions:                                │
   │   - Add new drug (modal)                    │
   │   - Edit drug info                          │
   │   - Delete drug                             │
   │   - Print barcode                           │
   │ ✓ Data source: localStorage (masterData)    │
   │   + API fallback: GET /api/drugs/           │
   └─────────────────────────────────────────────┘
   ┌────────────────────────────────────────────┐
   │ B. PRESCRIPTION.HTML (จ่ายยา)              │
   ├─────────────────────────────────────────────┤
   │ ✓ Display: Patient list (prescriptions)    │
   │ ✓ Select patient → Show:                   │
   │   - Doctor's orders (from prescription)    │
   │   - Current dispensing table                │
   │ ✓ Functions:                                │
   │   - Auto-fill from prescription            │
   │   - Add item to dispensing list            │
   │   - Save dispensing (POST /api/...)        │
   │ ✓ Data: Read from localStorage             │
   │   (chemo_prescriptions)                    │
   └─────────────────────────────────────────────┘
   ┌────────────────────────────────────────────┐
   │ C. RECEIVE.HTML (เบิก-รับยา)               │
   ├─────────────────────────────────────────────┤
   │ ✓ Display: Stock receive orders             │
   │ ✓ Functions:                                │
   │   - Create receive order                   │
   │   - Track incoming drugs + lots            │
   │   - Update stock levels                    │
   │ ✓ Data: API calls to Backend               │
   └─────────────────────────────────────────────┘
```

---

## **PART 2: CODE STRUCTURE ANALYSIS**

### **📝 LOGIN.HTML (Lines 1-211)**

**ฟังก์ชันหลัก:**

| ฟังก์ชัน | บรรทัด | ทำหน้าที่ | การทำงาน |
|---------|-------|---------|---------|
| `login-form.submit` | 130-172 | ล็อกอิน | 1. User input username/password → 2. POST to `/api/auth/login` → 3. Save JWT token + user data → 4. Redirect to index.html |
| `register-form.submit` | 175-208 | สมัครสมาชิก | 1. Validate password match → 2. POST to `/api/auth/register` → 3. Success alert + back to login |
| `toggleForms()` | 124-127 | Switch form | Toggle visibility between login and register sections |

**Data Flow:**
```
[User Input] → [Form Submit] → [Fetch API] → [Backend] → [JWT Token] → [localStorage] → [Redirect]
```

**Key localStorage Keys:**
- `access_token`: JWT token สำหรับ API calls
- `refresh_token`: สำหรับ refresh token
- `currentUser`: JSON ข้อมูลผู้ใช้ {user_id, full_name, role}

---

### **📊 MANAGE.HTML (Lines 900-1200+)**

**ฟังก์ชันหลัก:**

| ฟังก์ชัน | บรรทัด | ทำหน้าที่ |
|---------|-------|---------|
| `initializeMasterDrugData()` | 931-942 | โหลด DEFAULT_CANCER_DRUGS (10 ชนิด) เข้า masterData object |
| `loadDrugsFromStorage()` | 948-977 | ดึงยาจาก API (`GET /api/drugs/`) และ map ข้อมูล |
| `renderDrugListTable()` | 985-1007 | สร้าง table ของรายชื่อยา + color-code qty (red=0, orange=low, green=ok) |
| `selectDrug(row, code)` | 1069-1102 | เลือกยา → แสดงข้อมูลรายละเอียด + update tabs |
| `switchTab(tab)` | 1043-1065 | เปลี่ยน tab (general/details/expiry) |
| `renderLotTable()` | 1117-1142 | แสดงรายละเอียด lot + status |
| `renderExpiryTable()` | 1144-1176 | แสดงวันหมดอายุ + นับวันเหลือ + แจ้งเตือน |
| `searchDrugs(val)` | 1104-1111 | ค้นหาชื่อยา (case-insensitive) |

**Data Structure:**
```javascript
masterData = {
  'PD-00007': { 
    name, genericCode, genericName, barcode, unit,
    curQty, minQty, maxQty, usage, note, storage, routes, timeUse
  },
  'PD-00008': { ... }
}

lotData = {
  'PD-00007': [{ lot, type, exp, qty, note, status }]
}
```

**UI Components:**
- Left panel: Drug list (searchable + filterable)
- Right panel: Drug details (3 tabs)
  - Tab 1: General info + labels (Thai/English)
  - Tab 2: Lot information table
  - Tab 3: Expiry analysis
- Actions: Add, Edit, Delete, Print Barcode, Save, Print

---

### **💊 PRESCRIPTION.HTML (Lines 200-400+)**

**ฟังก์ชันหลัก:**

| ฟังก์ชัน | บรรทัด | ทำหน้าที่ |
|---------|-------|---------|
| `loadPatientList()` | 341-373 | โหลดรายชื่อผู้ป่วย จาก localStorage (`chemo_prescriptions`) |
| `loadDispensedPrescription(id, d)` | - | โหลดรายละเอียด prescription ที่เลือก |
| `autoFillFromPrescription()` | 226 | ดึงรายการยาจากใบสั่งแพทย์มาใส่ในตาราง dispensing |
| `addItem()` | 230 | เพิ่มรายการยาที่จะจ่ายลงตาราง |
| `saveDispensing()` | 291 | บันทึกการจ่ายยา → API call |
| `deletePatientEntry(id)` | 391 | ลบรายชื่อผู้ป่วยจาก list |

**Data Flow:**
```
[Prescription List] 
  ↓ (Select patient)
[Load Doctor's Orders]
  ↓ (Click auto-fill)
[Fill Dispensing Table]
  ↓ (Click save)
[POST /api/prescription/{id}/dispense]
  ↓
[Update stock qty in masterData]
  ↓
[Mark as dispensed]
```

**Key Tables:**
- Patient list table: HN, Name, Status, Items count
- Prescription items table: Drug code, Drug name, Quantity
- Dispensing items table: Item #, Drug name, Qty, mg, ml used, ml remaining

---

## **PART 3: CRITICAL FINDINGS & ISSUES** ⚠️

### **Issue 1: Mixed Data Sources (CRITICAL)**
```javascript
// ⚠️ PROBLEM: Uses BOTH localStorage AND API
loadDrugsFromStorage() {
  // Try API first
  const response = await fetch('http://127.0.0.1:8000/api/drugs/');
  
  // If API fails, fall back to localStorage
  // This creates data inconsistency
}
```

### **Issue 2: No Real-time Sync**
- Drug data saved in `localStorage` ≠ Backend database
- Changes in manage.html ≠ seen in prescription.html
- Need proper API integration

### **Issue 3: Security Issue (CRITICAL)**
```javascript
// ⚠️ JWT token visible in console + localStorage
localStorage.setItem('access_token', result.data.access_token);
// Should be HttpOnly cookie instead
```

### **Issue 4: Validation Missing**
- No server-side validation shown
- Frontend validation only (client-side can be bypassed)

---

## **PART 4: SUGGESTED IMPROVEMENTS** 💡

| ปัญหา | วิธีแก้ไข |
|------|---------|
| Mixed data sources | Use API only (remove localStorage masterData) |
| No real-time sync | Implement WebSocket or polling |
| Security issue | Use HttpOnly cookies for tokens |
| Missing validation | Add Pydantic validation on Backend |
| No error handling | Add try-catch + user-friendly errors |

---

## **PART 5: HTML FILES SUMMARY**

### **Files Overview:**

| ไฟล์ | หน้า | ฟังก์ชันหลัก | สถานะ |
|-----|------|---------|------|
| **login.html** | 211 | Authentication (Login/Register) | ✅ Ready for Backend |
| **index.html** | 300+ | Dashboard + Stats | ✅ Ready for Backend |
| **manage.html** | 1200+ | Master Drug Management | ⚠️ Uses localStorage fallback |
| **prescription.html** | 400+ | Drug Dispensing | ⚠️ Mixed API/localStorage |
| **receive.html** | 350+ | Drug Receiving | ✅ API-ready |
| **patients.html** | 250+ | Patient Management | ✅ API-ready |
| **dispense.html** | 300+ | Dispensing Records | ✅ API-ready |
| **status.html** | 200+ | System Status | ✅ Display only |
| **report.html** | 300+ | Reporting | ✅ API-ready |
| **users.html** | 250+ | User Management | ⚠️ RBAC rules shown |

---

**✅ วิเคราะห์เสร็จสมบูรณ์ - พร้อมรับคำสั่งถัดไป**
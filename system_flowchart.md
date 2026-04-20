# System Technical Flowchart

แผนภาพนี้แสดงความสัมพันธ์และการทำงานของฟังก์ชัน (JavaScript) และกระบวนการเข้าถึงข้อมูล (UI Logic) ในระบบปัจจุบัน

---

## 1. การทำงานเมื่อโหลดหน้าจอ (Initialization Flow)
ใช้ในหน้า: `manage.html`, `dispense.html`

```mermaid
graph TD
    A[User Opens Page] --> B{Event: DOMContentLoaded}
    B --> C[Query all elements with specific classes]
    C --> D[Loop: .day-select]
    D --> D1[Generate <option> 01-31]
    C --> E[Loop: .month-select]
    E --> E1[Generate <option> 01-12]
    C --> F[Loop: .year-select]
    F --> F1[Generate <option> 1900-2050 & 2450-2600]
    D1 & E1 & F1 --> G[Check data-value attribute]
    G --> H[Auto-select value if match]
```

---

## 2. การจัดการข้อมูลยา (Medicine Management Flow)
ใช้ในหน้า: `manage.html`

### 2.1 ระบบแท็บ (Tab Navigation)
```mermaid
graph LR
    A[User Clicks Tab Button] --> B[Call function switchTab-tabName]
    B --> C[Loop: Reset all tab styles & Hide all contents]
    C --> D[Set active style to clicked button]
    D --> E[Show content matching tabName]
```

### 2.2 ระบบหน้าต่างป๊อปอัพ (Modal Logic)
```mermaid
graph TD
    A[Click 'รายการใหม่' / Button] --> B[Call openModal]
    B --> C[Remove 'hidden' class from medicineModal]
    
    D[Click 'ยกเลิก' / 'X' Button] --> E[Call closeModal]
    E --> F[Add 'hidden' class to medicineModal]
    
    G[Click outside Modal Area] --> H{Event: window.onclick}
    H -- Target is Modal Background --> E
    H -- Target is Modal Content --> I[Do Nothing]
```

---

## 3. ผังความสัมพันธ์ของหน้าจอ (Navigation Flow)
แสดงการเชื่อมโยงระหว่างไฟล์ผ่าน Sidebar และ Header Tabs

```mermaid
graph TD
    Index[index.html - Dashboard] <--> Manage[manage.html - ข้อมูลยา]
    Manage <--> Receive[receive.html - เบิก-รับยา]
    Receive <--> Dispense[dispense.html - ใบสั่งยา]
    Dispense <--> Prescription[prescription.html - จ่ายยา]
    Prescription <--> Patients[patients.html - ทะเบียนผู้ป่วย]
    Patients <--> Status[status.html - เช็คสถานะ]
    Status <--> Report[report.html - รายงาน]
    Report <--> Index
```

---

## สรุปรายละเอียดทางเทคนิค
1.  **Event Handling:** ใช้ `addEventListener` สำหรับการเริ่มต้นหน้าจอ และ `onclick` สำหรับการตอบสนองทันที
2.  **DOM Manipulation:** เน้นการเปลี่ยนสถานะ Class (`hidden`) และการเปลี่ยน `className` ของ Element เพื่อเปลี่ยนรูปแบบการแสดงผล (CSS-driven UI)
3.  **Data Injection:** ใช้ `insertAdjacentHTML` เพื่อลดภาระการเขียน HTML ซ้ำซ้อนในส่วนของวันที่และเวลา
4.  **Scope:** ฟังก์ชันทั้งหมดยังเป็น Global Scope อยู่ภายในแต่ละไฟล์ (In-file scripts)

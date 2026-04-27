# การวิเคราะห์ตัวแปรและโครงสร้างโค้ด (Variable Analysis)

ระบบนี้ใช้ภาษา **JavaScript (ES6)** ในการพัฒนา โดยเขียนแบบฝัง (Embedded) ภายในไฟล์ HTML ไม่พบการใช้งาน TypeScript (.ts) ในโครงการนี้

---

## 1. ไฟล์: `Projest/manage.html` (หน้าจัดการข้อมูลยา)
**บทบาทหน้าที่:** จัดการหน้าจอข้อมูลยา, การเปิด-ปิด Modal และการสลับแท็บข้อมูล

| ตัวแปร / ฟังก์ชัน | ประเภท | หน้าที่ | บรรทัดที่ |
| :--- | :--- | :--- | :--- |
| `medicineModal` | ID | ใช้ระบุ Element ของหน้าต่างป๊อปอัพ (Modal) เพิ่มยาใหม่ | 14 |
| `openModal` | Function | ทำหน้าที่แสดง Modal เพิ่มยาใหม่ โดยการลบ class `hidden` | 684 |
| `closeModal` | Function | ทำหน้าที่ซ่อน Modal เพิ่มยาใหม่ โดยการเพิ่ม class `hidden` | 688 |

| `window.onclick` | Event | ตรวจจับการคลิกบนหน้าจอ เพื่อปิด Modal เมื่อคลิกพื้นที่ด้านนอก | 693 |
| `modal` | Local Var | เก็บ Element ของ `medicineModal` เพื่อตรวจสอบเป้าหมายการคลิก | 694 |
| `switchTab` | Function | ใช้สำหรับเปลี่ยนหน้าจอข้อมูล (Tab) เช่น ข้อมูลทั่วไป, รายละเอียดเพิ่มเติม | 700 |
| `tabName` | Parameter | รับชื่อแท็บที่ต้องการเปิด (เช่น 'general', 'details') | 700 |
| `tabs` | Const Array | รายการชื่อแท็บทั้งหมดที่มีอยู่ในหน้าจอ (`general`, `details`, `expiry`, `dispense`) | 702 |
| `tab-general` | ID | ปุ่มเลือกแท็บข้อมูลทั่วไป | 160 |
| `content-general`| ID | ส่วนเนื้อหาของแท็บข้อมูลทั่วไป | 175 |
| `DOMContentLoaded`| Event | ทำงานเมื่อโหลดหน้าเว็บเสร็จ เพื่อสร้าง Option วัน/เดือน/ปี ใน Select box | 710 |
| `select` | Loop Var | แทน Element `<select>` แต่ละตัวที่ถูกวนลูปมาจัดการ | 711 |
| `i`, `val` | Loop Var | ใช้สำหรับวนลูปสร้างตัวเลขวันที่ (1-31), เดือน (1-12) และปี | 712-713 |

---

## 2. ไฟล์: `Projest/dispense.html` (หน้าจัดการใบสั่งยา)
**บทบาทหน้าที่:** จัดการการเลือกวันที่ในแบบฟอร์มข้อมูลผู้ป่วย

| ตัวแปร / ฟังก์ชัน | ประเภท | หน้าที่ | บรรทัดที่ |
| :--- | :--- | :--- | :--- |
| `DOMContentLoaded`| Event | ทำงานเมื่อโหลดหน้าเว็บเสร็จ เพื่อสร้าง Option ใน Select box วัน/เดือน/ปี | 260 |
| `day-select` | Class | ใช้ระบุกลุ่ม `<select>` ที่ต้องการให้แสดงตัวเลือกวันที่ 01-31 | 261 |
| `month-select` | Class | ใช้ระบุกลุ่ม `<select>` ที่ต้องการให้แสดงตัวเลือกเดือน 01-12 | 268 |
| `year-select` | Class | ใช้ระบุกลุ่ม `<select>` ที่ต้องการให้แสดงตัวเลือกปี (พ.ศ. และ ค.ศ.) | 275 |
| `select` | Loop Var | แทน Element `<select>` ที่กำลังถูกจัดการใน Loop | 261 |

---

## 3. ไฟล์อื่นๆ (index, patients, prescription, receive, report, status)
**หมายเหตุ:** ไฟล์เหล่านี้ในปัจจุบันยังไม่มีการเขียน JavaScript Logic ซับซ้อน มีเพียงการเรียกใช้ Tailwind CSS ผ่าน CDN

| ตัวแปร / ฟังก์ชัน | ประเภท | หน้าที่ | ไฟล์ | บรรทัดที่ |
| :--- | :--- | :--- | :--- | :--- |
| `Tailwind CDN` | Script | ใช้สำหรับจัดสไตล์หน้าจอด้วย Tailwind CSS Classes | ทุกไฟล์ | 7 |

---

## สรุปภาพรวม (Technical Summary)
*   **ภาษาที่ใช้:** JavaScript (Vanilla JS)
*   **เทคนิคการเขียน:** 
    *   ใช้ `document.getElementById` และ `document.querySelectorAll` ในการเข้าถึง DOM
    *   ใช้ `classList.add/remove` ในการควบคุมการแสดงผล (Show/Hide)
    *   ใช้ `insertAdjacentHTML` ในการสร้าง UI Elements แบบ Dynamic (วันที่/เดือน/ปี)
    *   โครงสร้างเป็นแบบ **Client-side Rendering** พื้นฐานผ่านการสลับสถานะ CSS

ข้อมูลครบถ้วน พร้อมรับคำสั่งพัฒนาต่อแล้วครับครับ
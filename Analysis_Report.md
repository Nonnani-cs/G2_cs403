'# รายงานการวิเคราะห์ระบบจัดการสต็อกยาโรงพยาบาล (Hospital Medication Stock Management System)

เอกสารฉบับนี้สรุปผลการวิเคราะห์โครงสร้างและการทำงานของระบบในปัจจุบัน โดยอ้างอิงจากซอร์สโค้ดไฟล์ `replace_drugs_v3.py` และ `manage.html`

## 1. สถาปัตยกรรมของระบบ (System Architecture)
ระบบใช้รูปแบบ **Static HTML with Python Automation** โดยมีแนวคิดหลักคือ:
- **Frontend:** ใช้ไฟล์ HTML หลายไฟล์ที่ตกแต่งด้วย Tailwind CSS และ Lucide Icons
- **Backend Automation:** ใช้สคริปต์ Python ในการประมวลผลข้อมูลและแก้ไขไฟล์ HTML โดยตรง (Data Injection)
- **Data Persistence:** เตรียมรองรับการเชื่อมต่อกับ MySQL ผ่านสคริปต์ Python เพื่อนำข้อมูลมาอัปเดตลงในหน้าเว็บ

## 2. การทำงานของส่วนต่างๆ

### 2.1 ส่วนของ Python (Data Management Tool)
ไฟล์ `replace_drugs_v3.py` ทำหน้าที่เป็นเครื่องมือจัดการข้อมูลหลัก:
- **Data Storage:** เก็บข้อมูลรายชื่อยาแยกตามหมวดหมู่ในรูปแบบ List
- **HTML Templating:** สร้างโครงสร้างแถวของตาราง (`<tr>`) แบบไดนามิกพร้อมกำหนด Attributes ต่างๆ (เช่น `data-category`, `onclick`)
- **Automated Editing:** ใช้ Regex เพื่อค้นหาและแทนที่เนื้อหาในไฟล์ HTML ทำให้ไม่ต้องแก้ไขโค้ด HTML ด้วยมือเมื่อข้อมูลยาเปลี่ยนไป
- **Logic Injection:** ทำหน้าที่ฉีด (Inject) ฟังก์ชัน JavaScript ที่จำเป็นเข้าไปในไฟล์ HTML เพื่อให้หน้าเว็บทำงานได้สมบูรณ์

### 2.2 ส่วนของ HTML/JavaScript (Frontend UI)
ไฟล์ `manage.html` ทำหน้าที่แสดงผลและโต้ตอบกับผู้ใช้:
- **Layout Management:** ใช้ Sidebar ในการนำทาง และแบ่งส่วนจัดการข้อมูลเป็นระบบ Tabs (General, Details, Expiry)
- **Component-Based UI:**
    - **Modals:** ระบบหน้าต่าง Pop-up สำหรับเพิ่มยา, แก้ไขข้อมูล, และสั่งพิมพ์บาร์โค้ด
    - **Data Filtering:** ระบบกรองข้อมูลยาตามเงื่อนไข (อุณหภูมิห้อง/แช่เย็น/High Alert) และระบบค้นหาแบบ Real-time
- **Security & Authorization:** 
    - ตรวจสอบ Session จาก `localStorage`
    - ระบบ **Supervisor Override** เพื่อขอสิทธิ์ Senior Pharmacist ในการเข้าถึงฟังก์ชันสำคัญ เช่น การลบข้อมูล

## 3. ผังการไหลของข้อมูล (Data Flow)
1. **Database/Source:** ข้อมูลเริ่มต้นมาจาก MySQL (เตรียมการ) หรือ Python List
2. **Processing:** Python อ่านไฟล์ HTML -> ทำการประมวลผลข้อมูล -> เขียนข้อมูลใหม่ลงในไฟล์ HTML
3. **Rendering:** ผู้ใช้เปิดไฟล์ HTML ผ่าน Browser -> JavaScript ทำหน้าที่จัดการ Logic ภายในหน้าจอ (Tabs, Modals)
4. **Interaction:** เมื่อมีการคลิกเลือกยา ข้อมูลจาก `masterData` (ที่เตรียมไว้) จะถูกนำมาแสดงผลในส่วนรายละเอียด

## 4. สถานะปัจจุบันและจุดที่ควรพัฒนาต่อ
- **Data Linking:** ปัจจุบันข้อมูลถูก Hardcode อยู่ใน Python จำเป็นต้องเชื่อมต่อกับไฟล์ SQL จริงตามแผนที่วางไว้
- **File Paths:** เส้นทางไฟล์ในสคริปต์ Python ยังเป็นแบบระบุเจาะจง (Hardcoded Path) ควรปรับเป็น Relative Path เพื่อให้รันได้ทุกเครื่อง
- **Dynamic Updates:** ระบบปัจจุบันเป็นการอัปเดตไฟล์แบบ Manual Run สคริปต์ ซึ่งสามารถพัฒนาเป็นกึ่งอัตโนมัติได้เมื่อมีการเปลี่ยนแปลงข้อมูลใน Database

---
*วิเคราะห์การทำงานของระบบเรียบร้อย พร้อมรับคำสั่งพัฒนาต่อแล้วครับ*

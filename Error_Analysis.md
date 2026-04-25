# รายงานการวิเคราะห์ข้อผิดพลาด (Error Analysis Report)

เอกสารฉบับนี้ระบุข้อผิดพลาดสำคัญ 3 ประการที่พบในระบบจัดการยา (Frontend & Scripts) ตามที่ได้วิเคราะห์ไว้

---

## 1. ข้อผิดพลาดเรื่อง Path (Hardcoded Absolute Paths)
สคริปต์ Python มีการระบุที่อยู่ไฟล์แบบตายตัวซึ่งผูกติดกับเครื่องคอมพิวเตอร์ของผู้เขียนเดิม ทำให้ไม่สามารถรันบนเครื่องอื่นได้

| ไฟล์ (Python Script) | บรรทัดที่ | ตัวแปร/คำสั่ง | Path ที่ผิดพลาด |
|:---|:---:|:---|:---|
| `update_receive_table_logic.py` | 3 | `filepath` | `/Users/atcharapornn/Desktop/Projest/receive.html` |
| `update_receive_logic.py` | 3 | `filepath` | `/Users/atcharapornn/Desktop/Projest/receive.html` |
| `update_manage_labels.py` | 3 | `filepath` | `/Users/atcharapornn/Desktop/Projest/manage.html` |
| `replace_drugs_v3.py` | 46, 76 | `open()` | `/Users/atcharapornn/Desktop/Projest/manage.html` |
| `replace_drugs_v3.py` | 80, 110 | `open()` | `/Users/atcharapornn/Desktop/Projest/receive.html` |
| `fix_receive_table.py` | 3 | `filepath` | `/Users/atcharapornn/Desktop/Projest/receive.html` |
| `fix_manage_layout.py` | 3 | `filepath` | `/Users/atcharapornn/Desktop/Projest/manage.html` |
| `add_manage_interaction.py` | 4 | `filepath` | `/Users/atcharapornn/Desktop/Projest/manage.html` |

**ผลกระทบ:** สคริปต์จะเกิด Error `FileNotFoundError` ทันทีเมื่อรันในสภาพแวดล้อมอื่น

---

## 2. ข้อผิดพลาดเรื่องความเปราะบางของ Regex (Regex Fragility)
สคริปต์ `replace_drugs_v3.py` ใช้การค้นหาข้อความใน HTML ด้วย Regular Expression ซึ่งเสี่ยงต่อการทำงานผิดพลาดหากโครงสร้าง HTML เปลี่ยนไป

| ไฟล์ต้นทาง (Python) | บรรทัดที่ | Pattern ที่ใช้ค้นหา | ไฟล์เป้าหมาย (HTML) | จุดที่เชื่อมโยง |
|:---|:---:|:---|:---|:---|
| `replace_drugs_v3.py` | 49 | `r'<tbody id="drug-list-body".*?</tbody>'` | `manage.html` | บรรทัดที่ 335 (`<tbody id="drug-list-body">`) |
| `replace_drugs_v3.py` | 83 | `r'<tbody class="divide-y...".*?</tbody>'` | `receive.html` | บรรทัดที่ 347 (`<tbody>` ในตารางรับยา) |

**จุดที่ผิดพลาด:**
- หากใน `manage.html` มีการเปลี่ยน ID หรือเพิ่ม Attribute ในแท็ก `<tbody>` สคริปต์จะหาไม่เจอ
- ใน `receive.html` มีการใช้ `class="divide-y divide-gray-200"` หลายจุด (เช่น บรรทัด 260, 310) ทำให้ Regex อาจไปเขียนทับข้อมูลในตารางที่ผิดอัน

---

## 3. ข้อมูลไม่ตรงกันระหว่างฐานข้อมูลและหน้าเว็บ (Data Inconsistency)
ข้อมูลตัวอย่างที่สคริปต์ Python สร้างขึ้น ไม่ตรงกับข้อมูลที่นิยามไว้ในไฟล์ SQL Schema

### ความเชื่อมโยงที่ผิดพลาดของรหัสยา `PD-00007`:
- **ในไฟล์ SQL (`chemo_management.sql` บรรทัดที่ 140):**
  - รหัส: `PD-00007`
  - ชื่อยา: **Quinapril 10 mg**
- **ในไฟล์ Python (`replace_drugs_v3.py` บรรทัดที่ 24-25):**
  - การทำงาน: วนลูปสร้างยาตัวที่ 7 จาก List `room_temp_drugs`
  - ชื่อยาที่ได้: **Cetuximab** (ลำดับที่ 7 ใน List บรรทัดที่ 2)
- **ในไฟล์ HTML (`manage.html` หลังรันสคริปต์):**
  - แสดงผลเป็น: `PD-00007` | **Cetuximab**

**ผลกระทบ:** เมื่อมีการพัฒนา Backend เพื่อเชื่อมต่อฐานข้อมูลจริง จะเกิดความสับสนของข้อมูล (Data Mismatch) เนื่องจาก Frontend แสดงชื่อยาหนึ่ง แต่ Database เก็บข้อมูลเป็นอีกชื่อหนึ่งภายใต้รหัสเดียวกัน

---
*จัดทำเอกสารวิเคราะห์เรียบร้อย เพื่อใช้เป็นแนวทางในการแก้ไขก่อนเริ่มทำ Backend*

1. Paths (P0) — สภาพ: มี hardcoded Unix paths ในหลายสคริปต์ 
(แก้บางส่วนแล้ว)  
  - ความรุนแรง: Low → ถ้าเหลือจะไม่รันบน Windows  
  - แก้: ใช้ os.path.join(os.path.dirname(file), ...) 
(ทำไปแล้วบางไฟล์)
 2. Regex-based HTML edits — สภาพ: สคริปต์หลายไฟล์แก้ HTML ด้วย regex 
(fragile)  
  - ความรุนแรง: High → ทำให้เกิด <tbody> ซ้ำ, mismatched </div> และ 
layout แตก  
  - แก้: แปลงเป็น parser-based edits (BeautifulSoup / lxml). 
สำรองไฟล์ก่อนเขียน และมี dry-run
 3. Unclosed / mismatched HTML tags — สภาพ: manage.html, 
receive.html เคยมี mismatch / duplicate tbody / extra closing divs
  
  - ความรุนแรง: High (แสดงผล/JS พัง)  
  - แก้: ตรวจสอบ DOM ด้วย HTML parser, แก้โครงสร้าง DOM ให้ถูกต้อง
 4. Missing / inconsistent IDs and selectors — สภาพ: JS คาดหวัง id
 เช่น detail-code, receive-drug-code แต่ไม่ได้มาตรฐาน/หาย  
  - ความรุนแรง: Medium  
  - แก้: ระบุชุด IDs ที่ต้องการ, แก้ HTML ให้ตรงหรือแก้ JS เป็น 
event-delegation
 5. Inline onclick with unescaped data → XSS/JS errors — สภาพ: 
หลายไฟล์ใส่ onclick="select...('name')" โดยไม่ escape ทั้งชื่อ/quote  
  - ความรุนแรง: Medium → JS errors or XSS in hostile data  
  - แก้: ใช้ data-* attributes + event delegation หรือ escape 
ก่อนแทรก
 6. Script injection / script-block replacement fragile — สภาพ: 
tailwind CDN + logic scripts ถูกแทน/รวมผิดตำแหน่งในบางไฟล์  
  - ความรุนแรง: Medium  
  - แก้: แยก CDN tag ออกจาก logic script; แทรกด้วย DOM parser
 7. check_tags.py naive checker — สภาพ: ใช้ regex เพื่อเช็คแท็ก 
(ไม่รองรับ attributes/self-closing)  
  - ความรุนแรง: Low → ให้ใช้ lxml/BeautifulSoup หรือ tidy เพื่อ 
validate
 8. No backups & non-idempotent scripts — สภาพ: 
สคริปต์จำนวนมากเขียนไฟล์โดยตรง ไม่มี .bak / dry-run  
  - ความรุนแรง: High (risk data loss)  
  - แก้: ทุกสคริปต์ก่อนเขียนให้สร้าง .bak และมีโหมด dry-run
 9. Security: login.html stores plaintext mock users in 
localStorage  
  - ความรุนแรง: High for prod, Low for dev  
  - แก้: ให้เป็น mock-only (clear comment) หรือย้าย auth ไปเซิร์ฟเวอร์ + 
hash password
 10. SQL schema suggestions — สภาพ: chemo_management.sql 
โครงสร้างใช้ได้ แต่ไม่มี explicit INDEX บน FK  
  - ความรุนแรง: Low→Medium (performance)  
  - แก้: เพิ่ม INDEX บน fk (hn, drug_code, prescription_no, etc.)
 11. Script consolidation & version chaos — สภาพ: หลายไฟล์ 
fix_*/v2/v3/replace_drugs_* กระจัดกระจาย  
  - ความรุนแรง: Medium (maintenance burden)  
  - แก้: รวมเป็น update_system.py แยกฟังก์ชันย่อย, ลบไฟล์เก่าเมื่อทดสอบแล้ว
 12. Tests / CI missing — สภาพ: ไม่มี test/validator automation  
  - ความรุนแรง: Medium  
  - แก้: เพิ่ม scripts ตรวจ HTML validity, run dry-run patches, และ 
unit tests สำหรับ transform

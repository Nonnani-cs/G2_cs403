# แผนผังความสัมพันธ์ของตัวแปร (PlantUML Data Flow Diagram)

เอกสารฉบับนี้แสดงโค้ด PlantUML ที่จำลองการเชื่อมโยงของตัวแปรในระบบตามรายงานการวิเคราะห์การไหลของข้อมูล

---

## 1. PlantUML Code

คุณสามารถนำโค้ดด้านล่างนี้ไปวางใน [PlantText](https://www.planttext.com/) หรือ [PlantUML Online Server](https://www.plantuml.com/plantuml/) เพื่อดูภาพกราฟิกได้ครับ

```plantuml
@startuml
skinparam backgroundColor #fdfdfd
skinparam handwritten false
skinparam packageStyle rect
skinparam shadowing true

title Hospital Medication Stock - Detailed Data Flow Map

' Define Layers
package "Python Backend (Build Time)" #FFE0E0 {
    [replace_drugs_v3.py] as PY_Script
    entity "room_temp_drugs" as RT_Drugs <<List>>
    entity "refrigerated_drugs" as RF_Drugs <<List>>
}

package "Browser LocalStorage (Persistence)" #FFF4E0 {
    database "currentDispense" as LS_Dispense <<JSON>>
    database "currentUser" as LS_User <<Session>>
}

package "HTML / DOM Layer (UI)" #E0F0FF {
    node "manage.html" as HTML_Manage {
        [drug-list-body] as DOM_ManageBody
        entity "masterData" as JS_MasterManage <<Object>>
        artifact "selectDrug()" as JS_Select
    }
    
    node "receive.html" as HTML_Receive {
        [receive-drug-list-body] as DOM_ReceiveBody
        entity "masterData" as JS_MasterReceive <<Object>>
    }
    
    node "dispense.html" as HTML_Dispense {
        artifact "calculateResidual()" as JS_Calc
    }
    
    node "prescription.html" as HTML_Presc {
        [hn-input] as DOM_HN
    }
}

' --- Data Flow Connections ---

' 1. Python Injection Flow
RT_Drugs --> PY_Script : Provides names
RF_Drugs --> PY_Script : Provides names
PY_Script --> DOM_ManageBody : Injects <tr> rows\nvia Regex
PY_Script --> DOM_ReceiveBody : Injects <tr> rows\nvia Regex

' 2. User Interaction & State
DOM_ManageBody ..> JS_Select : onclick triggers
JS_MasterManage --> JS_Select : Provides detail data
JS_Select --> HTML_Manage : Updates Input Fields

' 3. Cross-Page Dispensing Flow
JS_Calc --> LS_Dispense : Writes calculated volume
LS_Dispense --> HTML_Presc : Read by window.onload
HTML_Presc --> DOM_HN : Populates Patient HN

' 4. Security & RBAC Flow
LS_User --> HTML_Manage : Checks role to unlock\nDelete button
LS_User --> HTML_Presc : Checks role for sidebar

' Legend / Notes
legend right
  |= Color |= Layer |
  |<#FFE0E0>| Python Automation |
  |<#FFF4E0>| LocalStorage |
  |<#E0F0FF>| HTML/JS Frontend |
endlegend

@enduml
```

---

## 2. คำอธิบายความสัมพันธ์ในไดอะแกรม

1.  **Python Layer (สีชมพู):** เป็นต้นทางของข้อมูลยา (Lists) ที่จะถูกสคริปต์ `replace_drugs_v3.py` นำไป "ฉีด" ลงใน DOM Elements ของไฟล์ HTML โดยตรง
2.  **HTML/DOM Layer (สีฟ้า):** 
    *   `masterData` ทำหน้าที่เป็นฐานข้อมูลจำลองภายในหน้าเว็บ
    *   `selectDrug()` คือตัวกลางที่คอยดึงข้อมูลจาก `masterData` มาแสดงบนหน้าจอเมื่อ User คลิกเลือกยา
    *   `calculateResidual()` คือตรรกะการคำนวณเคมีบำบัดหลัก
3.  **LocalStorage (สีส้ม):** เป็นสะพานเชื่อมระหว่างหน้าเว็บ
    *   `currentDispense` รับข้อมูลผลลัพธ์การคำนวณจากหน้าเบิกยา และส่งต่อให้หน้าพิมพ์ฉลาก
    *   `currentUser` เก็บสิทธิ์ของผู้ใช้เพื่อเปิด/ปิดฟังก์ชันตาม Role

---
*จัดทำแผนผัง PlantUML เรียบร้อย พร้อมรับคำสั่งพัฒนาต่อครับ*

-- ==============================================================================
-- ฐานข้อมูลระบบจัดการยาเคมีบำบัด (Chemotherapy Management System)
-- DBMS: MySQL / MariaDB
-- ==============================================================================

-- สร้างฐานข้อมูลและเลือกใช้งาน
CREATE DATABASE IF NOT EXISTS chemo_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE chemo_management;

-- ==============================================================================
-- 1. สร้างตารางผู้ใช้งานระบบ (users)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('Admin', 'Pharmacist', 'Staff') DEFAULT 'Pharmacist',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 2. สร้างตารางข้อมูลผู้ป่วย (patients)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS patients (
    hn VARCHAR(20) PRIMARY KEY COMMENT 'Hospital Number',
    prefix VARCHAR(20) NOT NULL COMMENT 'คำนำหน้าชื่อ',
    first_name VARCHAR(100) NOT NULL COMMENT 'ชื่อ',
    last_name VARCHAR(100) NOT NULL COMMENT 'นามสกุล',
    gender ENUM('ชาย', 'หญิง', 'อื่นๆ') NOT NULL,
    birth_date DATE NOT NULL,
    nationality VARCHAR(50) DEFAULT 'ไทย',
    weight DECIMAL(5,2) COMMENT 'น้ำหนักตัว (kg)',
    insurance_type VARCHAR(100) COMMENT 'สิทธิ์การรักษา',
    allergies TEXT COMMENT 'ประวัติการแพ้ยา',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 3. สร้างตารางข้อมูลยาพื้นฐาน (drugs)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS drugs (
    drug_code VARCHAR(20) PRIMARY KEY COMMENT 'รหัสยา เช่น PD-00007',
    barcode VARCHAR(50) UNIQUE COMMENT 'บาร์โค้ด',
    generic_name VARCHAR(255) NOT NULL COMMENT 'ชื่อสามัญทางยา',
    trade_name VARCHAR(255) NOT NULL COMMENT 'ชื่อทางการค้า',
    drug_group VARCHAR(100) COMMENT 'กลุ่มยา',
    unit VARCHAR(50) NOT NULL COMMENT 'หน่วยนับ เช่น เม็ด, ขวด',
    cost_price DECIMAL(10,2) DEFAULT 0.00 COMMENT 'ต้นทุน',
    selling_price DECIMAL(10,2) DEFAULT 0.00 COMMENT 'ราคาขาย',
    max_quantity INT DEFAULT 0 COMMENT 'จำนวนที่มีได้สูงสุด',
    min_quantity INT DEFAULT 0 COMMENT 'จุดสั่งซื้อเมื่อสินค้าเหลือ',
    is_high_alert BOOLEAN DEFAULT FALSE COMMENT 'เป็นยาอันตราย (High Alert) หรือไม่',
    total_stock INT DEFAULT 0 COMMENT 'จำนวนที่มีปัจจุบัน',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 4. สร้างตารางฉลากยา/วิธีใช้ (drug_labels)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS drug_labels (
    label_id INT AUTO_INCREMENT PRIMARY KEY,
    drug_code VARCHAR(20) NOT NULL,
    usage_instruction VARCHAR(255) COMMENT 'วิธีใช้ เช่น รับประทานครั้งละ 1 เม็ด',
    condition_of_use VARCHAR(255) COMMENT 'ใช้เมื่อมีอาการ',
    time_to_use VARCHAR(100) COMMENT 'เวลาที่ใช้ เช่น ก่อนอาหาร, หลังอาหาร',
    period VARCHAR(100) COMMENT 'ช่วงเวลา เช่น เช้า เย็น',
    storage_condition VARCHAR(255) COMMENT 'วิธีเก็บรักษา',
    note TEXT COMMENT 'หมายเหตุเพิ่มเติม',
    FOREIGN KEY (drug_code) REFERENCES drugs(drug_code) ON DELETE CASCADE
);

-- ==============================================================================
-- 5. สร้างตารางล็อตและวันหมดอายุของยา (drug_lots)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS drug_lots (
    lot_id INT AUTO_INCREMENT PRIMARY KEY,
    drug_code VARCHAR(20) NOT NULL,
    lot_number VARCHAR(50) NOT NULL,
    expiry_date DATE NOT NULL,
    quantity INT NOT NULL DEFAULT 0 COMMENT 'จำนวนคงเหลือใน Lot นี้',
    source_type ENUM('สั่งซื้อ', 'บริจาค', 'ยืม', 'อื่นๆ') DEFAULT 'สั่งซื้อ',
    status ENUM('ปกติ', 'ใกล้หมดอายุ', 'หมดอายุ') DEFAULT 'ปกติ',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drug_code) REFERENCES drugs(drug_code) ON DELETE CASCADE
);

-- ==============================================================================
-- 6. สร้างตารางใบสั่งยา (prescriptions)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_no VARCHAR(50) PRIMARY KEY COMMENT 'เลขที่ใบสั่งยา',
    hn VARCHAR(20) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL COMMENT 'ชื่อแพทย์ผู้สั่ง',
    prescription_date DATETIME NOT NULL COMMENT 'วันที่สั่งยา',
    insurance_used VARCHAR(100) COMMENT 'สิทธิ์รักษาที่ใช้ในบิลนี้',
    status ENUM('รอจ่ายยา', 'กำลังจัดยา', 'จ่ายยาแล้ว', 'ยกเลิก') DEFAULT 'รอจ่ายยา',
    dispensed_by INT COMMENT 'ผู้จ่ายยา (อ้างอิง user_id)',
    dispensed_at DATETIME NULL COMMENT 'เวลาที่จ่ายยาจริง',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (hn) REFERENCES patients(hn),
    FOREIGN KEY (dispensed_by) REFERENCES users(user_id)
);

-- ==============================================================================
-- 7. สร้างตารางรายการยาในใบสั่งยา (prescription_items)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS prescription_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    prescription_no VARCHAR(50) NOT NULL,
    drug_code VARCHAR(20) NOT NULL,
    quantity INT NOT NULL COMMENT 'จำนวนที่สั่ง',
    dose VARCHAR(50) COMMENT 'ขนาดยา เช่น 50 mg',
    duration VARCHAR(100) COMMENT 'ระยะเวลา เช่น 5 วัน',
    dispensed_lot_id INT NULL COMMENT 'Lot ที่ถูกนำมาจ่ายยา',
    FOREIGN KEY (prescription_no) REFERENCES prescriptions(prescription_no) ON DELETE CASCADE,
    FOREIGN KEY (drug_code) REFERENCES drugs(drug_code),
    FOREIGN KEY (dispensed_lot_id) REFERENCES drug_lots(lot_id)
);

-- ==============================================================================
-- 8. สร้างตารางบิลเบิก-รับยาเข้าคลัง (receive_orders)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS receive_orders (
    order_no VARCHAR(50) PRIMARY KEY COMMENT 'เลขที่บิล/เลขที่เบิก',
    order_date DATETIME NOT NULL COMMENT 'วันที่สั่งซื้อ/สร้างใบเบิก',
    expected_receive_date DATE NULL COMMENT 'นัดรับสินค้าวันที่',
    pharmacist_id INT NOT NULL COMMENT 'เภสัชกรผู้บันทึก',
    total_items INT DEFAULT 0 COMMENT 'จำนวนรายการทั้งหมด',
    total_amount DECIMAL(12,2) DEFAULT 0.00 COMMENT 'รวมเงินทั้งหมด',
    status ENUM('รอรับ', 'รับแล้วบางส่วน', 'รับครบแล้ว', 'ยกเลิก') DEFAULT 'รอรับ',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pharmacist_id) REFERENCES users(user_id)
);

-- ==============================================================================
-- 9. สร้างตารางรายการยาในบิลเบิก-รับยา (receive_order_items)
-- ==============================================================================
CREATE TABLE IF NOT EXISTS receive_order_items (
    receive_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(50) NOT NULL,
    drug_code VARCHAR(20) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT 'ราคาต่อหน่วยตอนสั่งซื้อ',
    ordered_quantity INT NOT NULL COMMENT 'จำนวนที่สั่ง',
    received_quantity INT DEFAULT 0 COMMENT 'จำนวนที่รับจริง',
    lot_number VARCHAR(50) NULL COMMENT 'Lot ที่รับเข้ามา',
    expiry_date DATE NULL COMMENT 'วันหมดอายุของ Lot นี้',
    FOREIGN KEY (order_no) REFERENCES receive_orders(order_no) ON DELETE CASCADE,
    FOREIGN KEY (drug_code) REFERENCES drugs(drug_code)
);

-- ==============================================================================
-- ส่วนการเพิ่มข้อมูลตัวอย่าง (Mock Data)
-- ==============================================================================

-- ข้อมูลผู้ใช้งาน
INSERT INTO users (username, password_hash, full_name, role) VALUES 
('admin01', 'hashed_password_here', 'เภสัชกร สมมุติ', 'Admin'),
('pharm01', 'hashed_password_here', 'เภสัชกร สมชาย ใจดี', 'Pharmacist'),
('pharm02', 'hashed_password_here', 'เภสัชกร สมหญิง แสงดี', 'Pharmacist');

-- ข้อมูลผู้ป่วย
INSERT INTO patients (hn, prefix, first_name, last_name, gender, birth_date, nationality, weight, insurance_type, allergies) VALUES 
('66001234', 'นาย', 'สมชาย', 'ใจดี', 'ชาย', '1987-07-25', 'ไทย', 65.5, 'สิทธิ์จ่ายตรงกรมบัญชีกลาง', 'ไม่พบประวัติการแพ้ยา'),
('66001235', 'นาง', 'สมหญิง', 'แสงดี', 'หญิง', '1990-05-15', 'ไทย', 52.0, 'ประกันสังคม', 'Penicillin');

-- ข้อมูลยาพื้นฐาน
INSERT INTO drugs (drug_code, barcode, generic_name, trade_name, drug_group, unit, cost_price, selling_price, max_quantity, min_quantity, is_high_alert, total_stock) VALUES 
('PD-00007', '8851234567890', 'Quinapril 10 mg', 'ACCUPRIL', 'ยาเคมีบำบัดกลุ่มที่ 1', 'เม็ด', 50.00, 75.00, 1000, 100, FALSE, 250),
('PD-00008', '8851234567891', 'Cyclophosphamide 500mg', 'Endoxan', 'Alkylating agents', 'ขวด', 450.00, 600.00, 200, 20, TRUE, 45),
('PD-00009', '8851234567892', 'Doxorubicin 50mg', 'Adriamycin', 'Anthracyclines', 'ขวด', 800.00, 1050.00, 150, 15, TRUE, 30),
('PD-00010', '8851234567893', '5-Fluorouracil 500mg', 'Adrucil', 'Antimetabolites', 'ขวด', 350.00, 500.00, 300, 50, TRUE, 40);

-- ฉลากยาและวิธีใช้
INSERT INTO drug_labels (drug_code, usage_instruction, condition_of_use, time_to_use, period, storage_condition, note) VALUES 
('PD-00007', 'รับประทานครั้งละ 1 เม็ด', '-', 'หลังอาหาร', 'เช้า เย็น', 'เก็บในที่แห้ง อุณหภูมิไม่เกิน 30 องศา', 'ระวังการใช้ร่วมกับยาความดันชนิดอื่น'),
('PD-00008', 'ใช้ฉีดเข้าหลอดเลือดดำ', 'ตามแพทย์สั่ง', '-', '-', 'เก็บในตู้เย็น 2-8 องศาเซลเซียส ป้องกันแสง', 'High Alert Drug - ต้องตรวจสอบสองครั้งก่อนบริหารยา');

-- ข้อมูลล็อตยา (Drug Lots)
INSERT INTO drug_lots (drug_code, lot_number, expiry_date, quantity, source_type, status) VALUES 
('PD-00007', 'LOT2024A', '2026-12-31', 250, 'สั่งซื้อ', 'ปกติ'),
('PD-00008', 'LOT2024001', '2026-12-31', 25, 'สั่งซื้อ', 'ปกติ'),
('PD-00008', 'LOT2024002', '2026-03-15', 20, 'สั่งซื้อ', 'ใกล้หมดอายุ'),
('PD-00009', 'LOT2024003', '2026-08-20', 30, 'สั่งซื้อ', 'ปกติ'),
('PD-00010', 'LOT2024004', '2026-10-10', 40, 'สั่งซื้อ', 'ปกติ');

-- ข้อมูลใบสั่งยา
INSERT INTO prescriptions (prescription_no, hn, doctor_name, prescription_date, insurance_used, status) VALUES 
('RX-2026-001', '66001234', 'นพ. เก่งกาจ สามารถ', '2026-02-07 11:00:00', 'สิทธิ์จ่ายตรงกรมบัญชีกลาง', 'รอจ่ายยา'),
('RX-2026-002', '66001235', 'พญ. ใจดี เมตตา', '2026-02-06 15:30:00', 'ประกันสังคม', 'จ่ายยาแล้ว');

-- รายการยาในใบสั่งยา
INSERT INTO prescription_items (prescription_no, drug_code, quantity, dose, duration, dispensed_lot_id) VALUES 
('RX-2026-001', 'PD-00008', 1, '500 mg', '1 วัน', NULL),
('RX-2026-002', 'PD-00010', 2, '500 mg', '1 วัน', 5);

-- ข้อมูลบิลเบิก-รับยาเข้าคลัง
INSERT INTO receive_orders (order_no, order_date, expected_receive_date, pharmacist_id, total_items, total_amount, status) VALUES 
('REQ-2026-001', '2026-02-05 10:00:00', '2026-02-07', 2, 1, 4500.00, 'รับครบแล้ว'),
('REQ-2026-002', '2026-02-01 14:15:00', '2026-02-05', 3, 1, 4000.00, 'รับครบแล้ว');

-- รายการยาในบิลเบิก-รับยา
INSERT INTO receive_order_items (order_no, drug_code, unit_price, ordered_quantity, received_quantity, lot_number, expiry_date) VALUES 
('REQ-2026-001', 'PD-00008', 450.00, 10, 10, 'LOT2024001', '2026-12-31'),
('REQ-2026-002', 'PD-00009', 800.00, 5, 5, 'LOT2024003', '2026-08-20');

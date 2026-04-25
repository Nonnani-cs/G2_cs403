# Hospital Medication Stock Management System - Project Connections

This document explains how the files in the `Projest/` directory connect to each other and the variables that link them.

## 1. Project Overview
The project is a **Chemotherapy Management System** consisting of:
- **Frontend:** Static HTML files styled with Tailwind CSS and Lucide icons.
- **Database:** A MySQL schema defining the data structure for drugs, patients, and orders.
- **Automation/Maintenance:** Python scripts used to transform and update the HTML files.

## 2. File Connections (Navigation)
All HTML files are connected via a **Sidebar Navigation Menu**. Each file contains links (`<a>` tags) to the other main pages.

| File | Role | Main Connections (HTML) |
|------|------|-------------------------|
| `index.html` | Dashboard | Links to all other pages |
| `manage.html` | Stock Management | Links to `receive.html`, `dispense.html`, etc. |
| `receive.html` | Drug Receiving | Links to `manage.html`, `dispense.html`, etc. |
| `dispense.html` | Manage Prescriptions | Links to `manage.html`, `receive.html`, etc. |
| `prescription.html` | Dispense & Labels | Links to `patients.html`, `status.html`, etc. |
| `patients.html` | Patient Registry | Links to `status.html`, `report.html`, etc. |
| `status.html` | Stock Status | Links to all other pages |
| `report.html` | Reports | Links to all other pages |

## 3. Python to HTML Connections (Modification Scripts)
The Python scripts in this project are tools that modify the HTML files. They use a variable (usually `filepath`) to target specific files.

| Python Script | Targeted Variable / File | Line Number | Action |
|---------------|--------------------------|-------------|--------|
| `replace_drugs_v3.py` | `manage.html`, `receive.html` | 46, 80 | Injects drug lists and JS filters |
| `update_receive_logic.py`| `receive.html` | 3 | Updates logic for receiving drugs |
| `fix_manage_layout.py` | `manage.html` | 3 | Adjusts CSS/HTML layout |
| `add_dispense_drug_list.py`| `dispense.html` | 3 | Adds drug list to dispense page |
| `remove_sidebar_links.py`| All `.html` files | 5 | Removes specific nav links |

## 4. Variable Connections (Data & IDs)
These variables/IDs are used across different files to ensure consistent data display and behavior.

### A. Python Data Variables (In `replace_drugs_v3.py`)
- **`room_temp_drugs`** (Line 1): List of drugs stored at room temperature.
- **`refrigerated_drugs`** (Line 8): List of drugs requiring refrigeration.
- These variables are used to generate the HTML table rows injected into `manage.html` and `receive.html`.

### B. HTML Element IDs (Targeted by JS and Python)
- **`drug-list-body`**: In `manage.html`, used by Python (Line 49 of `replace_drugs_v3.py`) and JS (Line 63 of `replace_drugs_v3.py`) to manage the drug table.
- **`receive-drug-list-body`**: In `receive.html`, used by Python (Line 83 of `replace_drugs_v3.py`) and JS (Line 97 of `replace_drugs_v3.py`).
- **`drug-filter`**: In `manage.html`, the ID for the dropdown that filters drugs (Line 51 of `replace_drugs_v3.py`).

### C. JavaScript Functions (Injected into HTML)
- **`filterDrugs(category)`**: Injected into `manage.html` (Line 62 of `replace_drugs_v3.py`).
- **`filterReceiveDrugs(category)`**: Injected into `receive.html` (Line 96 of `replace_drugs_v3.py`).
- **`selectDrug(element, code, name)`**: Injected into `manage.html` (Line 24 of `replace_drugs_v3.py`).
- **`selectDrugReceive(element, code, name, ...)`**: Injected into `receive.html` (Line 36 of `replace_drugs_v3.py`).

## 5. Database Schema (In `chemo_management.sql`)
The SQL file defines the following tables which correspond to the data seen in the HTML files:
- **`drugs`** (Line 35): Stores drug codes (e.g., `PD-00007`), names, and stock levels.
- **`patients`** (Line 18): Stores HN (Hospital Number) and patient details.
- **`drug_lots`** (Line 71): Stores expiry dates and lot numbers.

---
*End of Analysis*

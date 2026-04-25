import os
import re

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clear value="..." but keep placeholder
    content = re.sub(r'value="[^"]*"', 'value=""', content)

    # 2. Clear tbody content for major tables
    # Target common tbody IDs or just all tbodies that look like they have mock data
    content = re.sub(r'(<tbody.*?>)(.*?)(</tbody\s*>)', r'\1\3', content, flags=re.DOTALL)

    # 3. Clear JS mock data arrays/objects
    # Target common names: masterData, historyData, mockBills, checkoutList, prescriptions, drugInventory, etc.
    patterns = [
        r'const\s+masterData\s*=\s*\[.*?\]\s*;',
        r'const\s+historyData\s*=\s*\{.*?\}\s*;',
        r'const\s+mockBills\s*=\s*\[.*?\]\s*;',
        r'let\s+checkoutList\s*=\s*\[.*?\]\s*;',
        r'const\s+prescriptions\s*=\s*\[.*?\]\s*;',
        r'const\s+drugInventory\s*=\s*\[.*?\]\s*;',
        r'const\s+patients\s*=\s*\[.*?\]\s*;'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, lambda m: m.group(0).split('=')[0] + '= [];' if '[' in m.group(0) else m.group(0).split('=')[0] + '= {};', content, flags=re.DOTALL)

    # 4. Remove initialization calls in window.onload or end of script
    init_calls = [
        r'initMasterTable\(.*?\);',
        r'renderCheckoutTable\(.*?\);',
        r'renderHistoryTable\(.*?\);',
        r'initPatientTable\(.*?\);',
        r'loadPrescriptions\(.*?\);'
    ]
    
    for call in init_calls:
        content = re.sub(call, f'// {call} // Removed mock init', content)

    # Specific fix for receive.html window.onload if exists
    content = re.sub(r'window\.onload\s*=\s*\(.*?\)\s*=>\s*\{.*?\}', r'window.onload = () => { lucide.createIcons(); };', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    files_to_clean = [
        'receive.html', 'manage.html', 'dispense.html', 
        'prescription.html', 'patients.html', 'status.html', 'report.html'
    ]
    for f in files_to_clean:
        if os.path.exists(f):
            clean_file(f)

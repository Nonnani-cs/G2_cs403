import re

filepath = '/Users/atcharapornn/Desktop/Projest/receive.html'
with open(filepath, 'r') as f:
    content = f.read()

# Reconstruct the drug list with proper <td> tags and onclick handlers
drug_data = [
    ("PD-00001", "Cyclophosphamide 500mg", ""),
    ("PD-00002", "Doxorubicin 50mg", "995"),
    ("PD-00003", "5-Fluorouracil 500mg", ""),
    ("PD-00004", "Cisplatin 50mg", ""),
    ("PD-00005", "Paclitaxel 100mg", "1396"),
    ("PD-00006", "Carboplatin 150mg", "997"),
    ("PD-00007", "Vincristine 1mg", "1497"),
    ("PD-00008", "Epirubicin 50mg", "1100"),
    ("PD-00009", "Gemcitabine 1g", ""),
    ("PD-00010", "Oxaliplatin 50mg", ""),
    ("PD-00011", "Methotrexate 50mg", "1000"),
    ("PD-00012", "Docetaxel 20mg", ""),
    ("PD-00013", "Ifosfamide 1g", ""),
    ("PD-00014", "Etoposide 100mg", ""),
    ("PD-00015", "Bleomycin 15 units", ""),
    ("PD-00016", "Mitomycin C 10mg", ""),
    ("PD-00017", "Cytarabine 100mg", ""),
    ("PD-00018", "Vinblastine 10mg", ""),
    ("PD-00019", "Irinotecan 100mg", ""),
    ("PD-00020", "Pemetrexed 500mg", ""),
    ("PD-00021", "Capecitabine 500mg", "1000"),
]

rows_html = ""
for code, name, stock in drug_data:
    row_class = "bg-blue-600 text-white cursor-pointer" if code == "PD-00007" else "hover:bg-blue-50 cursor-pointer"
    border_class = "border-white" if code == "PD-00007" else "border-gray-200"
    rows_html += f'                            <tr class="{row_class}" onclick="selectDrugReceive(this, \'{code}\', \'{name}\')">'
    rows_html += f'<td class="p-1 border-r {border_class}">{code}</td>'
    rows_html += f'<td class="p-1 border-r {border_class}">{name}</td>'
    rows_html += f'<td class="p-1 text-right">{stock}</td></tr>\n'

# Replace the broken tbody
content = re.sub(
    r'<tbody class="divide-y divide-gray-200">.*?</tbody>',
    f'<tbody class="divide-y divide-gray-200">\n{rows_html}                        </tbody>',
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Receive table fixed.")

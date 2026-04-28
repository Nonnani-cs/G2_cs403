import os
import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

filepath = os.path.join(current_dir, 'manage.html')
with open(filepath, 'r') as f:
    content = f.read()

# Add IDs to inputs
content = re.sub(
    r'<input type="text" class="w-1/2 border border-gray-300 p-1 bg-white outline-none" value="8850339007520">',
    r'<input type="text" id="detail-barcode" class="w-1/2 border border-gray-300 p-1 bg-white outline-none" value="8850339007520">',
    content
)

content = re.sub(
    r'<input type="text" class="w-1/3 border border-gray-300 p-1 bg-gray-100 outline-none" value="QUINA">',
    r'<input type="text" id="detail-generic-code" class="w-1/3 border border-gray-300 p-1 bg-gray-100 outline-none" value="QUINA">',
    content
)

content = re.sub(
    r'<input type="text" class="flex-1 border border-gray-300 p-1 bg-gray-100 outline-none" value="QUINALAPRIL">',
    r'<input type="text" id="detail-generic-name" class="flex-1 border border-gray-300 p-1 bg-gray-100 outline-none" value="QUINALAPRIL">',
    content
)

content = re.sub(
    r'<input type="text" class="w-1/4 border border-gray-300 p-1 bg-gray-100 outline-none" value="07">',
    r'<input type="text" id="detail-group-code" class="w-1/4 border border-gray-300 p-1 bg-gray-100 outline-none" value="07">',
    content
)

content = re.sub(
    r'<input type="text" class="flex-1 border border-gray-300 p-1 bg-gray-100 outline-none" value="ANTIHYPERTENSIVES">',
    r'<input type="text" id="detail-group-name" class="flex-1 border border-gray-300 p-1 bg-gray-100 outline-none" value="ANTIHYPERTENSIVES">',
    content
)

content = re.sub(
    r'<input type="text" class="w-full border border-gray-300 p-1 bg-white outline-none" value="285">',
    r'<input type="text" id="detail-price" class="w-full border border-gray-300 p-1 bg-white outline-none" value="285">',
    content,
    count=1
)

content = re.sub(
    r'<textarea class="w-full h-12 border border-gray-300 p-1 outline-none resize-none">วันละ 1 ครั้ง หลังอาหารกลางวัน</textarea>',
    r'<textarea id="detail-label-usage" class="w-full h-12 border border-gray-300 p-1 outline-none resize-none">วันละ 1 ครั้ง หลังอาหารกลางวัน</textarea>',
    content
)

content = re.sub(
    r'<textarea class="w-full h-10 border border-gray-300 p-1 outline-none resize-none">ทานยาทุกวันจนหมดและดื่มน้ำตามมากๆ</textarea>',
    r'<textarea id="detail-label-note" class="w-full h-10 border border-gray-300 p-1 outline-none resize-none">ทานยาทุกวันจนหมดและดื่มน้ำตามมากๆ</textarea>',
    content
)

# Replace the selectDrug function with a more comprehensive one
new_func = """
        function selectDrug(row, code, name) {
            // Remove active class from all rows
            const rows = document.querySelectorAll('#drug-list-body tr');
            rows.forEach(r => {
                r.className = 'hover:bg-blue-50 cursor-pointer text-gray-800';
            });
            
            // Add active class to clicked row
            row.className = 'bg-blue-600 text-white cursor-pointer hover:bg-blue-700';
            
            // Update details
            const detailCode = document.getElementById('detail-code');
            const detailName = document.getElementById('detail-name');
            if (detailCode) detailCode.value = code;
            if (detailName) detailName.value = name;

            // Generate mock data for the rest of general info
            const barcode = document.getElementById('detail-barcode');
            if(barcode) barcode.value = '8850' + code.replace('PD-', '') + '990';
            
            const gCode = document.getElementById('detail-generic-code');
            const gName = document.getElementById('detail-generic-name');
            if(gCode) gCode.value = name.substring(0, 4).toUpperCase();
            if(gName) gName.value = name.split(' ')[0].toUpperCase();

            const grpCode = document.getElementById('detail-group-code');
            const grpName = document.getElementById('detail-group-name');
            if(grpCode) grpCode.value = '09';
            if(grpName) grpName.value = 'ANTINEOPLASTIC AGENTS';

            const price = document.getElementById('detail-price');
            // Mock price based on code
            let mockPrice = (parseInt(code.replace('PD-', '')) * 150) + 500;
            if(price) price.value = mockPrice;

            const usage = document.getElementById('detail-label-usage');
            if(usage) usage.value = 'ฉีดเข้าหลอดเลือดดำตามแผนการรักษาของแพทย์';
            
            const note = document.getElementById('detail-label-note');
            if(note) note.value = 'เป็นยาอันตราย ต้องบริหารโดยบุคลากรทางการแพทย์ที่เชี่ยวชาญ';
            
            // Generate mock expiry and lot data for selected drug
            const lotTbody = document.getElementById('lot-list-body');
            if (lotTbody) {
                lotTbody.innerHTML = `
                    <tr class="hover:bg-gray-50 transition-colors">
                        <td class="py-4 px-2 font-medium whitespace-nowrap">${name}</td>
                        <td class="py-4 px-2 whitespace-nowrap">LOT2026_${code}</td>
                        <td class="py-4 px-2">
                            <span class="border border-blue-400 text-blue-600 px-3 py-0.5 rounded-full text-xs font-bold whitespace-nowrap">ซื้อ</span>
                        </td>
                        <td class="py-4 px-2 whitespace-nowrap">2026-12-31</td>
                        <td class="py-4 px-2 text-center whitespace-nowrap">50 ขวด</td>
                        <td class="py-4 px-2 text-blue-700">สั่งซื้อจากบริษัท ${code}</td>
                        <td class="py-4 px-2 whitespace-nowrap">
                            <span class="inline-block bg-gray-100 text-gray-600 px-3 py-1 rounded-md text-xs font-bold whitespace-nowrap">ปกติ</span>
                        </td>
                    </tr>
                `;
            }

            const expiryTbody = document.getElementById('expiry-list-body');
            if (expiryTbody) {
                expiryTbody.innerHTML = `
                    <tr class="hover:bg-gray-50 transition-colors">
                        <td class="py-4 px-2 font-medium">${name}</td>
                        <td class="py-4 px-2">LOT2026_${code}</td>
                        <td class="py-4 px-2">31/12/2026</td>
                        <td class="py-4 px-2 text-center">50</td>
                        <td class="py-4 px-2">
                            <span class="flex items-center text-green-600 font-bold">
                                <span class="mr-1.5 border border-green-600 rounded-full w-5 h-5 flex items-center justify-center text-[10px]">✓</span> OK
                            </span>
                        </td>
                        <td class="py-4 px-2 text-gray-600">เภสัชกร สมมุติ</td>
                    </tr>
                `;
            }
        }
"""

content = re.sub(
    r'function selectDrug\(row, code, name\) \{.*?\}(?=\s*</script>)',
    new_func.strip(),
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)
print("Done")

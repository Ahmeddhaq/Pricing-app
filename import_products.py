import os
import django
import sys
import openpyxl

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricing_app.settings")
django.setup()

from core.models import MasterProduct

wb = openpyxl.load_workbook('2025 Price worksheet - Mark.xlsx', data_only=True)
sheet = wb.active

added = 0
for row_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
    if row_idx < 4: # Skip headers
        continue
    
    product_name = row[0]
    viscosity = row[2]
    api_acea = row[3]
    spec_rec = row[4]
    item_number = row[5]
    case_size = row[6]
    liters_per_case = row[7]

    if not item_number:
        continue

    try:
        item_number = str(item_number).strip()
        MasterProduct.objects.update_or_create(
            code=item_number,
            defaults={
                'description': str(product_name).strip() if product_name else '',
                'viscosity': str(viscosity).strip() if viscosity else '',
                'specification': str(api_acea).strip() if api_acea else '',
                'approval': str(spec_rec).strip() if spec_rec else '',
                'packaging': str(case_size).strip() if case_size else '',
                'liters_per_case': float(liters_per_case) if liters_per_case else None,
            }
        )
        added += 1
    except Exception as e:
        print(f"Error on row {row_idx}: {e}")

print(f"Added/Updated {added} products.")

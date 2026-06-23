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
current_name = ""
current_sub = ""
current_viscosity = ""
current_spec = ""
current_approval = ""

seen_rows = set()

for row_idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):
    if row_idx < 4: # Skip headers
        continue
    
    raw_name = str(row[0]).strip() if row[0] is not None else ""
    raw_sub = str(row[1]).strip() if row[1] is not None else ""
    raw_viscosity = str(row[2]).strip() if row[2] is not None else ""
    raw_spec = str(row[3]).strip() if row[3] is not None else ""
    raw_approval = str(row[4]).strip() if row[4] is not None else ""
    item_number = str(row[5]).strip() if row[5] is not None else ""
    case_size = str(row[6]).strip() if row[6] is not None else ""
    liters_per_case = row[7]

    if not item_number:
        continue

    # Carry forward logic
    if raw_name:
        current_name = raw_name
        current_sub = ""
        current_viscosity = ""
        current_spec = ""
        current_approval = ""

    if raw_sub:
        current_sub = raw_sub
    if raw_viscosity:
        current_viscosity = raw_viscosity
    if raw_spec:
        current_spec = raw_spec
    if raw_approval:
        current_approval = raw_approval

    if current_sub:
        combined_description = f"{current_name} {current_sub}".strip()
    else:
        combined_description = current_name.strip()

    seen_key = (
        item_number,
        combined_description.lower(),
        current_viscosity.lower(),
        current_spec.lower(),
        current_approval.lower(),
        case_size.lower()
    )

    if seen_key in seen_rows:
        continue
    seen_rows.add(seen_key)

    try:
        MasterProduct.objects.update_or_create(
            code=item_number,
            description=combined_description,
            packaging=case_size,
            defaults={
                'viscosity': current_viscosity,
                'specification': current_spec,
                'approval': current_approval,
                'liters_per_case': float(liters_per_case) if liters_per_case else None,
            }
        )
        added += 1
    except Exception as e:
        print(f"Error on row {row_idx}: {e}")

print(f"Added/Updated {added} products.")

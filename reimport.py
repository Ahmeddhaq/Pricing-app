import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pricing_app.settings")
django.setup()

from core.models import MasterProduct, Product

print("Clearing MasterProduct and Product tables...")
mp_count, _ = MasterProduct.objects.all().delete()
p_count, _ = Product.objects.all().delete()
print(f"Deleted {mp_count} MasterProducts and {p_count} Products.")

print("Running product import...")
import import_products
print("Clean import complete!")

from django.contrib import admin

from .models import ExportFile, Product, ProductChange


admin.site.register(Product)
admin.site.register(ProductChange)
admin.site.register(ExportFile)
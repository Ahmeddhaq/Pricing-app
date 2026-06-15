from decimal import Decimal

from django.conf import settings
from django.db import models


class MasterProduct(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Product Code")
    description = models.CharField(max_length=200, verbose_name="Description")
    viscosity = models.CharField(max_length=100, blank=True, verbose_name="Viscosity")
    specification = models.CharField(max_length=200, blank=True, verbose_name="Specification")
    approval = models.CharField(max_length=200, blank=True, verbose_name="Approval")
    packaging = models.CharField(max_length=100, blank=True, verbose_name="Packaging")
    liters_per_case = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Liters per case")

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pricing_records.update(name=self.description)


class Product(models.Model):
    master = models.ForeignKey(MasterProduct, on_delete=models.CASCADE, null=True, blank=True, related_name="pricing_records")
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    production_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    profit_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_products",
    )
    updated_at = models.DateTimeField(auto_now=True)
    effective_date = models.DateField(null=True, blank=True)

    def calculate_selling_price(self):
        return (self.production_price + (self.production_price * self.profit_percent / Decimal("100"))).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        if self.master:
            self.name = self.master.description
        self.selling_price = self.calculate_selling_price()
        super().save(*args, **kwargs)


class ProductChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="changes")
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ExportFile(models.Model):
    file = models.FileField(upload_to="exports/")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ImportFile(models.Model):
    file = models.FileField(upload_to="imports/")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    template_mode = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    error_summary = models.JSONField(null=True, blank=True)

class Quotation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="quotations")
    salesperson = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quotations")
    customer_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_final_price(self):
        discount = self.product.selling_price * self.discount_percent / Decimal("100")
        return ((self.product.selling_price - discount) * self.quantity).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        if not self.final_price:
            self.final_price = self.calculate_final_price()
        super().save(*args, **kwargs)


class Pricing(models.Model):
    product = models.ForeignKey(MasterProduct, on_delete=models.CASCADE, related_name="pricings", verbose_name="Product")
    packaging = models.CharField(max_length=100, blank=True, verbose_name="Packaging")
    production_cost_per_liter = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Production Cost Per Liter")
    production_cost_date = models.DateTimeField(auto_now=True, verbose_name="Production Cost Date")
    final_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Final Cost")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Selling Price")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Quantity")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Price")
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Discount")

    def __str__(self):
        return f"Pricing for {self.product.code}"


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    message = models.TextField()
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="read_notifications", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Lead(models.Model):
    STAGE_CHOICES = (
        ('New', 'New'),
        ('Qualified', 'Qualified'),
        ('Proposition', 'Proposition'),
        ('Won', 'Won'),
    )

    salesperson = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leads")
    contact_name = models.CharField(max_length=255, verbose_name="Contact Name")
    opportunity_name = models.CharField(max_length=255, verbose_name="Opportunity Name")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Contact Email")
    contact_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Contact Phone")
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Revenue (AED)")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.opportunity_name} - {self.contact_name}"

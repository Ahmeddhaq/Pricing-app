from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ExportFile, Product


class ProductTests(TestCase):
    def test_selling_price_is_calculated(self):
        product = Product.objects.create(
            sku="SKU-1",
            name="Engine Oil",
            quantity=10,
            production_price=100,
            profit_percent=15,
        )
        self.assertEqual(str(product.selling_price), "115.00")


class ExportTests(TestCase):
    def test_export_creates_file_record(self):
        user = User.objects.create_user(username="user", password="pass")
        Product.objects.create(
            sku="SKU-1",
            name="Engine Oil",
            quantity=10,
            production_price=100,
            profit_percent=15,
        )
        self.client.login(username="user", password="pass")
        response = self.client.get(reverse("export_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ExportFile.objects.count(), 1)
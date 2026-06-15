from django import forms

from .models import Product, Lead


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["sku", "name", "quantity", "production_price", "profit_percent"]


class PriceUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["quantity", "production_price"]


class ImportForm(forms.Form):
    file = forms.FileField()

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["contact_name", "opportunity_name", "contact_email", "contact_phone", "revenue", "stage"]
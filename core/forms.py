import re

from django import forms

from .models import DriverLead, InvestorLead

PHONE_RE = re.compile(r"^\+?[0-9\s\-\(\)]{7,20}$")


class _StyledFormMixin:
    """Applies the shared `.field-input` class to every widget automatically."""

    def _style_fields(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " field-input").strip()


class DriverLeadForm(_StyledFormMixin, forms.ModelForm):
    class Meta:
        model = DriverLead
        fields = ["name", "email", "phone_number"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Jane Doe", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "jane@example.com", "autocomplete": "email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+1 555 123 4567", "autocomplete": "tel"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone


class InvestorLeadForm(_StyledFormMixin, forms.ModelForm):
    class Meta:
        model = InvestorLead
        fields = [
            "name", "phone_number", "email", "date_of_registration",
            "offer_type", "car_brand", "car_model", "car_year", "expected_price",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Jane Doe", "autocomplete": "name"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+1 555 123 4567", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"placeholder": "jane@example.com", "autocomplete": "email"}),
            "date_of_registration": forms.DateInput(attrs={"type": "date"}),
            "offer_type": forms.Select(),
            "car_brand": forms.TextInput(attrs={"placeholder": "Toyota"}),
            "car_model": forms.TextInput(attrs={"placeholder": "Prius"}),
            "car_year": forms.NumberInput(attrs={"placeholder": "2013", "min": 1980, "max": 2100}),
            "expected_price": forms.NumberInput(attrs={"placeholder": "12000", "min": 0, "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"].strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone
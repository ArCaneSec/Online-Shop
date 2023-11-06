from django import forms

from .models import Order


class OrderCreateForm(forms.Form):
    """This form responsible for creating orders."""
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
        ]
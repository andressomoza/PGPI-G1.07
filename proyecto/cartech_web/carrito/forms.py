# forms.py
from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, label='Card Number')
    expiry_month = forms.CharField(max_length=2, label='Expiry Month')
    expiry_year = forms.CharField(max_length=4, label='Expiry Year')
    cvc = forms.CharField(max_length=4, label='CVC')

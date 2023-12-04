# forms.py
from django import forms
from shop.models import Eleccion, Coche, Accesorio, DireccionUsuario
from pedidos.models import Pedido

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, label='Card Number')
    expiry_month = forms.CharField(max_length=2, label='Expiry Month')
    expiry_year = forms.CharField(max_length=4, label='Expiry Year')
    cvc = forms.CharField(max_length=4, label='CVC')

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre', 'apellidos', 'email', 'direccion', 'ciudad', 'codigo_postal']

class DatosEnvioForm(forms.ModelForm):
    class Meta:
        model = DireccionUsuario
        fields = ['direccion', 'ciudad', 'codigo_postal']

class DatosClienteForm(forms.Form):
    nombre = forms.CharField()
    apellidos = forms.CharField()
    email = forms.CharField()
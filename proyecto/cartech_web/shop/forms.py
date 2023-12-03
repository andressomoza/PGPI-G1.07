# En forms.py (crea este archivo si no lo tienes)
from django import forms
from .models import Coche

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['marca', 'modelo', 'combustible', 'conduccion', 'consumo', 'stock', 'caballos', 'precio_inicial', 'imagen']

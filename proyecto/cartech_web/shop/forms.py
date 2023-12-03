# En forms.py (crea este archivo si no lo tienes)
from django import forms
from .models import Coche, Accesorio

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = ['marca', 'modelo', 'combustible', 'conduccion', 'consumo', 'stock', 'caballos', 'precio_inicial', 'imagen']


class AccesorioForm(forms.ModelForm):
    class Meta:
        model = Accesorio
        fields = ['nombre','stock', 'precio','imagen']

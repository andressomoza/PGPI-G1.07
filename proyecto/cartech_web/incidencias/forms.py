from django import forms
from .models import Incidencia

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'urgencia']
        
class IncidenciaEditForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['estado']
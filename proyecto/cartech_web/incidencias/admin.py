from django.contrib import admin
from .models import Incidencia

#register
@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'urgencia']


    


from django.contrib import admin
from .models import Incidencia

#register
@admin.register(Incidencia)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'urgencia']


    


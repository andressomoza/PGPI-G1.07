from django.contrib import admin
from .models import Coche, Accesorio, Eleccion

#register
    
@admin.register(Coche)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'combustible', 'conduccion', 'consumo', 'caballos', 'precio_inicial']

@admin.register(Accesorio)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['precio', 'nombre']

@admin.register(Eleccion)
class ProductAdmin(admin.ModelAdmin):
    pass
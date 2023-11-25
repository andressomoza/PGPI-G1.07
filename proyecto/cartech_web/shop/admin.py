from django.contrib import admin
from .models import Category, Product, Coche, Accesorio, Eleccion

#register
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Coche)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'combustible', 'conduccion', 'consumo', 'caballos', 'precio_inicial']

@admin.register(Accesorio)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['precio', 'nombre']

@admin.register(Eleccion)
class ProductAdmin(admin.ModelAdmin):
    pass
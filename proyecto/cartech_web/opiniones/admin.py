from django.contrib import admin
from .models import Opinion

#register
@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'descripcion','valoracion']


    


from django.contrib import admin
from .models import Pedido

#register
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['status']


    


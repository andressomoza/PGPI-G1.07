from django.contrib import admin
from django.urls import path
from . import views

app_name = 'pedidos'  # Agrega esta línea

urlpatterns = [
    #path('new', views.crear_pedido, name='crear_pedido'),
    path('list', views.listar_pedidos, name='listar_pedidos'),
]

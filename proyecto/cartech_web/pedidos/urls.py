from django.contrib import admin
from django.urls import path
from . import views

app_name = 'pedidos'  # Agrega esta línea

urlpatterns = [
    path('', views.listar_pedidos, name='listar_pedidos'),
    path('<int:id>/', views.detalle_pedido, name='detalle_pedido'),
]

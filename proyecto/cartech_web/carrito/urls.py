from django.contrib import admin
from django.urls import path
from . import views

app_name = 'carrito'  # Agrega esta línea

urlpatterns = [
    path('', views.listar_carrito, name='listar_carrito'),
]

from django.contrib import admin
from django.urls import path
from . import views

app_name = 'incidencias'  # Agrega esta línea

urlpatterns = [
    path('listar_incidencias', views.incidencias_list, name='incidencias_list'),
    path('crear_incidencia/', views.crear_incidencia, name='crear_incidencia'),
]

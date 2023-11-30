from django.contrib import admin
from django.urls import path
from . import views

app_name = 'incidencias'  # Agrega esta línea

urlpatterns = [
    path('', views.pagina_base, name='base'),
    path('listar_incidencias', views.listar_incidencias, name='listar_incidencias'),
    path('crear_incidencia', views.crear_incidencia, name='crear_incidencia'),
]

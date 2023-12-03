from django.contrib import admin
from django.urls import path
from . import views

app_name = 'incidencias'  # Agrega esta línea

urlpatterns = [
    path('', views.pagina_base, name='base'),
    path('list', views.listar_incidencias, name='listar_incidencias'),
    path('new', views.crear_incidencia, name='crear_incidencia'),
    path('me', views.mis_incidencias, name='mis_incidencias'),
]

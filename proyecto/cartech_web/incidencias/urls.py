from django.contrib import admin
from django.urls import path
from . import views

app_name = 'incidencias' 

urlpatterns = [
    path('', views.pagina_base, name='pagina_base'),
    path('list', views.listar_incidencias, name='listar_incidencias'),
    path('new', views.crear_incidencia, name='crear_incidencia'),
    path('me', views.mis_incidencias, name='mis_incidencias'),
    path('delete/<int:id>', views.borrar_incidencia, name='borrar_incidencia'),
    path('new/<int:id_pedido>', views.crear_incidencia_pedido, name='crear_incidencia_pedido'),
    
]

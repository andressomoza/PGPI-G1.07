from django.contrib import admin
from django.urls import path
from . import views

app_name = 'opiniones' 

urlpatterns = [
    path('', views.pagina_base, name='pagina_base'),
    path('list', views.listar_opiniones, name='listar_opiniones'),
    path('new/<int:id_eleccion>', views.crear_opinion, name='crear_opinion'),
    path('me', views.mis_opiniones, name='mis_opiniones'),
    path('elecciones/', views.mis_elecciones, name='mis_elecciones'),
    path('delete/<int:id>', views.borrar_opinion, name='borrar_opinion'),
    
]

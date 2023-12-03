from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
   
    path('', views.home, name='home'),
    
    path('coches/new', views.crear_coche, name='crear_coche'),
    path('coches/delete/<int:id>', views.borrar_coche, name='borrar_coche'),
    path('coches/edit/<int:id>', views.editar_coche, name='editar_coche'),
    path('coches/selector', views.selector, name='selector'),
    path('coches/list', views.listado_coches, name='listado_coches'),
    path('coches/list/combustible', views.listado_combustible, name='listado_combustible'),
    path('coches/list/electricos', views.listado_electricos, name='listado_electricos'),
    path('coches/list/hibridos', views.listado_hibridos, name='listado_hibridos'),
    path('coches/<int:id>/', views.detalles_coche, name='detalles_coche'),
    
    path('accesorios/new', views.crear_accesorio, name='crear_accesorio'),
    path('accesorios/<int:id>/', views.detalles_accesorio, name='detalles_accesorio'),
    path('accesorios/delete/<int:id>', views.borrar_accesorio, name='borrar_accesorio'),
    path('accesorios/edit/<int:id>', views.editar_accesorio, name='editar_accesorio'),
    path('accesorios/list', views.listado_accesorios, name='listado_accesorios'),

]
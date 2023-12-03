from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    #path('', views.product_list, name='product_list'),
    path('', views.home, name='home'),
    path('new', views.crear_coche, name='crear_coche'),
    path('delete/<int:id>', views.borrar_coche, name='borrar_coche'),
    path('edit/<int:id>', views.editar_coche, name='editar_coche'),
    path('selector', views.selector, name='selector'),
    path('list/all', views.listado_coches, name='listado_coches'),
    path('list/combustible', views.listado_combustible, name='listado_combustible'),
    path('list/electricos', views.listado_electricos, name='listado_electricos'),
    path('list/hibridos', views.listado_hibridos, name='listado_hibridos'),
    path('<int:id>/', views.detalles, name='car_detail'),

]
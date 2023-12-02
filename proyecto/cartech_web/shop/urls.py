from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    #path('', views.product_list, name='product_list'),
    path('', views.home, name='home'),
    path('list', views.cars_list, name='cars_list'),
    path('<int:id>/', views.car_detail, name='car_detail'),
    path('agregar/<int:eleccion_id>', views.agregar_eleccion, name='add'),
    path('eliminar/<int:eleccion_id>', views.eliminar_eleccion, name='remove'),
    path('limpiar/<int:eleccion_id>', views.limpiar_carrito, name='clean')
]
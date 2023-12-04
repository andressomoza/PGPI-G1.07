from django.contrib import admin
from django.urls import path
from . import views
from .views import PaymentView


app_name = 'carrito'

urlpatterns = [
    path('', views.listar_carrito, name='listar_carrito'),
    path('make_payment/', PaymentView.as_view(), name='make_payment'),
    path('add/<int:eleccion_id>', views.add, name='add'),
    path('delete/<int:eleccion_id>', views.delete, name='delete'),
    path('checkout/', views.checkout, name="checkout")
]

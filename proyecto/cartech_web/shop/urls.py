from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    #path('', views.product_list, name='product_list'),
    path('', views.cars_list, name='carslist'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
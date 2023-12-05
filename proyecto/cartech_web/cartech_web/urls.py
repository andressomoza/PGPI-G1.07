from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    path('incidencias/', include('incidencias.urls', namespace='incidencias')),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('opiniones/', include('opiniones.urls', namespace='opiniones')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('salir/', views.salir, name='salir'),
    path('signup/', views.signup, name='signup'),
    path('carrito/', include('carrito.urls', namespace='carrito')),
    #path('api-auth/', include('rest_framework.urls')),  # Include DRF's authentication URLs

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'cartech_web.views.bad_request'
handler403 = 'cartech_web.views.forbidden'
handler404 = 'cartech_web.views.not_found'
handler500 = 'cartech_web.views.internal_server_error'

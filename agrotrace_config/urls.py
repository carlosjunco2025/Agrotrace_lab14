from django.contrib import admin
from django.urls import path, include

from agrotrace.urls import router

# Semana 13: rutas de las apps de estructura inicial. Cada app expone un
# endpoint de metadata hasta que los modelos de negocio se escriban en S14.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/catalogo/', include('catalogo.urls')),
    path('api/pedidos/', include('pedidos.urls')),
    path('api/productores/', include('productores.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/comercializacion/', include('comercializacion.urls')),
    path('api/trazabilidad/', include('trazabilidad.urls')),
    path('agrotrace/', include('agrotrace.urls')),
]

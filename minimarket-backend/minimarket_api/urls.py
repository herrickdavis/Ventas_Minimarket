from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/catalogo/', include('catalogo.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/gestion/', include('gestion.urls')),
    path('api/finanzas/', include('finanzas.urls')),
    path('api/seguridad/', include('seguridad.urls')),
    
    # Autenticación
    path('api/auth-token/', authtoken_views.obtain_auth_token, name='api_auth_token'),
]
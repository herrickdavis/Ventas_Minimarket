from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, PermissionViewSet, RegistroActividadViewSet

router = DefaultRouter()
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'roles', GroupViewSet, basename='rol')
router.register(r'permisos', PermissionViewSet, basename='permiso')
router.register(r'registros-actividad', RegistroActividadViewSet, basename='registroactividad')

urlpatterns = [
    path('', include(router.urls)),
]
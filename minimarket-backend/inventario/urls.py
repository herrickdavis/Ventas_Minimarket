from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UbicacionViewSet, MovimientoStockViewSet, AjusteStockViewSet

router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet, basename='ubicacion')
router.register(r'movimientos-stock', MovimientoStockViewSet, basename='movimientostock')
router.register(r'ajustes-stock', AjusteStockViewSet, basename='ajustestock')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MetodoPagoViewSet, TransaccionCajaViewSet, GastoViewSet

router = DefaultRouter()
router.register(r'metodos-pago', MetodoPagoViewSet, basename='metodopago')
router.register(r'transacciones-caja', TransaccionCajaViewSet, basename='transaccioncaja')
router.register(r'gastos', GastoViewSet, basename='gasto')

urlpatterns = [
    path('', include(router.urls)),
]
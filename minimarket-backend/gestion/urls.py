from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProveedorViewSet, OrdenCompraViewSet, OrdenCompraItemViewSet, 
    ClienteViewSet, SesionPOSViewSet, VentaViewSet, VentaItemViewSet, 
    CarritoViewSet, CarritoItemViewSet
)

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'ordenes-compra', OrdenCompraViewSet, basename='ordencompra')
router.register(r'ordenes-compra-items', OrdenCompraItemViewSet, basename='ordencompraitem')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'sesiones-pos', SesionPOSViewSet, basename='sesionpos')
router.register(r'ventas', VentaViewSet, basename='venta')
router.register(r'venta-items', VentaItemViewSet, basename='ventaitem')
router.register(r'carritos', CarritoViewSet, basename='carrito')
router.register(r'carrito-items', CarritoItemViewSet, basename='carritoitem')

urlpatterns = [
    path('', include(router.urls)),
]
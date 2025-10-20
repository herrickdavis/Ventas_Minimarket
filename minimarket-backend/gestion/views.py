from django.shortcuts import render


from rest_framework import viewsets, permissions
from .models import (
    Proveedor, OrdenCompra, OrdenCompraItem, Cliente, 
    SesionPOS, Venta, VentaItem, Carrito, CarritoItem
)
from .serializers import (
    ProveedorSerializer, OrdenCompraSerializer, OrdenCompraItemSerializer, 
    ClienteSerializer, SesionPOSSerializer, VentaSerializer, VentaItemSerializer, 
    CarritoSerializer, CarritoItemSerializer
)

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.prefetch_related('items').all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrdenCompraItemViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompraItem.objects.all()
    serializer_class = OrdenCompraItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class SesionPOSViewSet(viewsets.ModelViewSet):
    queryset = SesionPOS.objects.all()
    serializer_class = SesionPOSSerializer
    permission_classes = [permissions.IsAuthenticated]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.prefetch_related('items').all()
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

class VentaItemViewSet(viewsets.ModelViewSet):
    queryset = VentaItem.objects.all()
    serializer_class = VentaItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.prefetch_related('items').all()
    serializer_class = CarritoSerializer
    permission_classes = [permissions.AllowAny]

class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer
    permission_classes = [permissions.AllowAny]
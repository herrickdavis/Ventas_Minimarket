from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Ubicacion, MovimientoStock, AjusteStock
from .serializers import UbicacionSerializer, MovimientoStockSerializer, AjusteStockSerializer

class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head', 'options'] # Ledger es solo lectura via API

class AjusteStockViewSet(viewsets.ModelViewSet):
    queryset = AjusteStock.objects.all()
    serializer_class = AjusteStockSerializer
    permission_classes = [permissions.IsAuthenticated]
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import MetodoPago, TransaccionCaja, Gasto
from .serializers import MetodoPagoSerializer, TransaccionCajaSerializer, GastoSerializer

class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransaccionCajaViewSet(viewsets.ModelViewSet):
    queryset = TransaccionCaja.objects.all()
    serializer_class = TransaccionCajaSerializer
    permission_classes = [permissions.IsAuthenticated]

class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    permission_classes = [permissions.IsAuthenticated]
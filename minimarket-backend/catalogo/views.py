from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import (
    Categoria, Marca, ClaseImpuesto, Unidad, ConversionUnidad, 
    Producto, VarianteProducto, ComboProducto, ListaPrecios, ReglaListaPrecios
)
from .serializers import (
    CategoriaSerializer, MarcaSerializer, ClaseImpuestoSerializer, UnidadSerializer, 
    ConversionUnidadSerializer, ProductoSerializer, VarianteProductoSerializer, 
    ComboProductoSerializer, ListaPreciosSerializer, ReglaListaPreciosSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClaseImpuestoViewSet(viewsets.ModelViewSet):
    queryset = ClaseImpuesto.objects.all()
    serializer_class = ClaseImpuestoSerializer
    permission_classes = [permissions.IsAuthenticated]

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversionUnidadViewSet(viewsets.ModelViewSet):
    queryset = ConversionUnidad.objects.all()
    serializer_class = ConversionUnidadSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.prefetch_related('variantes', 'items_combo').all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class VarianteProductoViewSet(viewsets.ModelViewSet):
    queryset = VarianteProducto.objects.all()
    serializer_class = VarianteProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ComboProductoViewSet(viewsets.ModelViewSet):
    queryset = ComboProducto.objects.all()
    serializer_class = ComboProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ListaPreciosViewSet(viewsets.ModelViewSet):
    queryset = ListaPrecios.objects.all()
    serializer_class = ListaPreciosSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReglaListaPreciosViewSet(viewsets.ModelViewSet):
    queryset = ReglaListaPrecios.objects.all()
    serializer_class = ReglaListaPreciosSerializer
    permission_classes = [permissions.IsAuthenticated]
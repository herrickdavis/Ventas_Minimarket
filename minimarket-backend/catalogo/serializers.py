from rest_framework import serializers
from .models import (
    Categoria, Marca, ClaseImpuesto, Unidad, ConversionUnidad, 
    Producto, VarianteProducto, ComboProducto, ListaPrecios, ReglaListaPrecios
)

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ClaseImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseImpuesto
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = '__all__'

class ConversionUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionUnidad
        fields = '__all__'

class VarianteProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VarianteProducto
        fields = '__all__'

class ComboProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    variantes = VarianteProductoSerializer(many=True, read_only=True)
    items_combo = ComboProductoSerializer(many=True, read_only=True)
    
    categoria = serializers.StringRelatedField()
    marca = serializers.StringRelatedField()
    unidad_base = serializers.StringRelatedField()

    class Meta:
        model = Producto
        fields = [
            'id', 'sku', 'nombre', 'descripcion', 'tipo', 'marca', 'categoria', 
            'clase_impuesto', 'unidad_base', 'es_vendible', 'es_comprable', 
            'es_producto_fisico', 'umbral_bajo_stock', 'imagen_url', 
            'creado_en', 'actualizado_en', 'variantes', 'items_combo'
        ]

class ListaPreciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaPrecios
        fields = '__all__'

class ReglaListaPreciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReglaListaPrecios
        fields = '__all__'
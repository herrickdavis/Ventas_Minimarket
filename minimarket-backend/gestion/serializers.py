from rest_framework import serializers
from .models import (
    Proveedor, OrdenCompra, OrdenCompraItem, Cliente, 
    SesionPOS, Venta, VentaItem, Carrito, CarritoItem
)

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class OrdenCompraItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenCompraItem
        fields = '__all__'

class OrdenCompraSerializer(serializers.ModelSerializer):
    items = OrdenCompraItemSerializer(many=True, read_only=True)
    proveedor = serializers.StringRelatedField()
    creado_por = serializers.StringRelatedField()

    class Meta:
        model = OrdenCompra
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class SesionPOSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionPOS
        fields = '__all__'

class VentaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaItem
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    items = VentaItemSerializer(many=True, read_only=True)
    cliente = serializers.StringRelatedField()
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Venta
        fields = '__all__'

class CarritoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoItem
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True, read_only=True)
    class Meta:
        model = Carrito
        fields = '__all__'
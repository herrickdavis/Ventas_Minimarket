from rest_framework import serializers
from .models import Ubicacion, MovimientoStock, AjusteStock

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class MovimientoStockSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()
    variante = serializers.StringRelatedField()
    ubicacion = serializers.StringRelatedField()
    unidad = serializers.StringRelatedField()
    creado_por = serializers.StringRelatedField()
    documento = serializers.StringRelatedField()

    class Meta:
        model = MovimientoStock
        fields = '__all__'

class AjusteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = AjusteStock
        fields = '__all__'
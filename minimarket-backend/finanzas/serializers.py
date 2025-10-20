from rest_framework import serializers
from .models import MetodoPago, TransaccionCaja, Gasto

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class TransaccionCajaSerializer(serializers.ModelSerializer):
    metodo_pago = serializers.StringRelatedField()
    creado_por = serializers.StringRelatedField()
    documento = serializers.StringRelatedField()
    
    class Meta:
        model = TransaccionCaja
        fields = '__all__'

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'
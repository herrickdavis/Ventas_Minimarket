from rest_framework import serializers
from .models import RegistroActividad
from django.contrib.auth.models import User, Group, Permission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups']
        read_only_fields = ['id']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']
        read_only_fields = ['id']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'content_type', 'codename']
        read_only_fields = ['id']

class RegistroActividadSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    objeto = serializers.StringRelatedField()
    
    class Meta:
        model = RegistroActividad
        fields = [
            'id', 'usuario', 'accion', 'objeto', 'datos_anteriores', 
            'datos_nuevos', 'ip', 'user_agent', 'creado_en'
        ]
        read_only_fields = fields
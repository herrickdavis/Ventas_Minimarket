from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import RegistroActividad
from .serializers import RegistroActividadSerializer, UserSerializer, GroupSerializer, PermissionSerializer
from django.contrib.auth.models import User, Group, Permission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class RegistroActividadViewSet(viewsets.ModelViewSet):
    queryset = RegistroActividad.objects.all()
    serializer_class = RegistroActividadSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get', 'head', 'options']
from django.shortcuts import render
from rest_framework import viewsets
from myapp.models import Cliente, Especialista, Admin
from myapp.api_crud.serializers import ClienteSerializer, EspecialistaSerializer, AdminSerializer
from rest_framework.permissions import IsAdminUser

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class EspecialistaViewSet(viewsets.ModelViewSet):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminUser]
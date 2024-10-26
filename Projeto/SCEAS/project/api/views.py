from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import Usuario, Veiculo
from .serializers import UsuarioSerializer, VeiculoSerializer

# Create your views here.

# View para listar ou criar usuários
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# View para visualizar, atualizar ou deletar um usuário
class UsuarioViewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# View para listar ou criar veículos
class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

# View para visualizar, atualizar ou deletar um veículo
class VeiculoViewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
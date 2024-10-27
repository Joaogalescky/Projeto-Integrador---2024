from django.shortcuts import render
from rest_framework import generics

from firebase_config import db
from .models import Usuario, Veiculo
from .serializers import UsuarioSerializer, VeiculoSerializer

# Create your views here.

# View para listar ou criar usuários
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        usuario = serializer.save()  # Salva o usuário no banco de dados
        # Adiciona o usuário no Firebase
        firebase_data = {
            "nome": usuario.nome,
            "telefone": usuario.telefone,
            "email": usuario.email,
            "veiculos": [
                {
                    "placa": veiculo.placa,
                    "modelo": veiculo.modelo,
                    "marca": veiculo.marca,
                    "cor": veiculo.cor,
                }
                for veiculo in usuario.veiculos.all()
            ]
        }
        db.collection('usuarios').document(str(usuario.id)).set(firebase_data)

# View para visualizar, atualizar ou deletar um usuário
class UsuarioUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def perform_update(self, serializer):
        usuario = serializer.save()
        # Atualiza o usuário no Firebase
        firebase_data = {
            "nome": usuario.nome,
            "telefone": usuario.telefone,
            "email": usuario.email,
            "veiculos": [
                {
                    "placa": veiculo.placa,
                    "modelo": veiculo.modelo,
                    "marca": veiculo.marca,
                    "cor": veiculo.cor,
                }
                for veiculo in usuario.veiculos.all()
            ]
        }
        db.collection('usuarios').document(str(usuario.id)).set(firebase_data)

    # Exclui o usuário do Firebase antes de remover do banco de dados local
    def perform_destroy(self, instance):
        db.collection('usuarios').document(str(instance.id)).delete()
        instance.delete()

# View para listar ou criar veículos
class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

# View para visualizar, atualizar ou deletar um veículo
class VeiculoUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

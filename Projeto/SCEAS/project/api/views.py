from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from firebase_config import db

from .models import Usuario, Veiculo
from .serializers import UserSerializer, UsuarioSerializer, VeiculoSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Página inicial
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

# Função de login
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login realizado com sucesso"})
        else:
            return JsonResponse({"success": False, "message": "Credenciais inválidas"})
    
    return render(request, 'login.html')

# Função de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# View para criação de usuários (login)
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público a este endpoint

# View para registro de usuários com criação de token
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público a este endpoint

    def perform_create(self, serializer):
        # Salva o usuário no banco de dados
        user = serializer.save()

        # Cria o token para o novo usuário
        token, created = Token.objects.get_or_create(user=user)

        # Retorna os dados do usuário e o token
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

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
    
    def perform_create(self, serializer):
        veiculo = serializer.save()
        # Atualiza no Firebase (opcional, se quiser)
        db.collection('veiculos').document(str(veiculo.id)).set({
            "placa": veiculo.placa,
            "modelo": veiculo.modelo,
            "marca": veiculo.marca,
            "cor": veiculo.cor,
        })

# View para visualizar, atualizar ou deletar um veículo
class VeiculoUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    
    def perform_update(self, serializer):
        veiculo = serializer.save()
        # Atualiza o veículo no Firebase
        db.collection('veiculos').document(str(veiculo.id)).set({
            "placa": veiculo.placa,
            "modelo": veiculo.modelo,
            "marca": veiculo.marca,
            "cor": veiculo.cor,
        })

    def perform_destroy(self, instance):
        # Exclui o veículo do Firebase
        db.collection('veiculos').document(str(instance.id)).delete()
        instance.delete()

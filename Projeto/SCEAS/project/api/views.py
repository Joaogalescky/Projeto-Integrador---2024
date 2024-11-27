from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Usuario, Veiculo
from .serializers import UserSerializer, UsuarioSerializer, VeiculoSerializer
from firebase_config import db

# Página inicial protegida
@login_required(login_url='login')  # Redireciona para a página de login se o usuário não estiver autenticado
def home(request):
    return render(request, 'home.html')


# Login de Usuário
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            # Verifica se o email está cadastrado
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado")
            return render(request, "login.html")

        # Autentica o usuário pelo username (necessário no Django)
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial
        else:
            messages.error(request, "Credenciais inválidas")  # Mostra mensagem de erro
            return render(request, 'login.html')

    return render(request, "login.html")


# Função de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Cadastro de Usuário
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'register.html')

        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Usuário registrado com sucesso. Faça login!")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Erro ao registrar usuário: " + str(e))

    return render(request, 'register.html')

# View para criação de usuários (login)
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público a este endpoint

# View para registro de novos usuários
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público a este endpoint

    def perform_create(self, serializer):
        user = serializer.save()  # Salva o usuário no banco de dados
        token, created = Token.objects.get_or_create(user=user)  # Cria o token para o novo usuário

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

    def perform_destroy(self, instance):
        # Remove o usuário do Firebase
        db.collection('usuarios').document(str(instance.id)).delete()
        instance.delete()

# View para listar ou criar veículos
class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

    def perform_create(self, serializer):
        veiculo = serializer.save()
        # Atualiza no Firebase (opcional)
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
        # Remove o veículo do Firebase
        db.collection('veiculos').document(str(instance.id)).delete()
        instance.delete()

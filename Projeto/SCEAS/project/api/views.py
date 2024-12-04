from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Usuario, Veiculo
from .serializers import UserSerializer, UsuarioSerializer, VeiculoSerializer
from firebase_config import db

def home(request):
    if request.user.is_authenticated:
        return render(request, 'html/Home.html')
    else:
        return redirect('login')

def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'html/Profile.html', {'user': request.user})
    else:
        return redirect('login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Verifica se o email já está em uso
        if User.objects.filter(email=email).exists():
            return render(request, 'html/Register.html', {'error': 'Email já em uso'})
        
        user = User.objects.create_user(email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'html/Register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Autentica o usuário com email e senha
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'html/Login.html', {'error': 'Email ou senha inválidos'})
    return render(request, 'html/Login.html')

# def logout_view(request):
#     logout(request)
#     return redirect('login')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            send_mail(
                'Solicitação de Reset de Senha',
                f'Por favor, clique no link abaixo para resetar sua senha: {request.build_absolute_uri("/reset-password/")}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return render(request, 'html/ForgotPassword.html', {'message': 'Instruções do reset da senha foram enviados ao seu email.'})
        except User.DoesNotExist:
            return render(request, 'html/ForgotPassword.html', {'error': 'Nenhum usuário com esse email foi encontrado.'})
    return render(request, 'html/ForgotPassword.html')

# Criação de usuários (registro)
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público

    def perform_create(self, serializer):
        user = serializer.save()  # Salva o usuário no banco de dados
        token, _ = Token.objects.get_or_create(user=user)  # Cria o token para o novo usuário

        # Retorna os dados do usuário e o token
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


# Login e retorno do token
class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('username')
        password = request.data.get('password')

        # Autenticar usuário
        user = authenticate(username=email, password=password)
        if user is not None:
            # Se usuário autenticado, retorna o token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key
            }, status=status.HTTP_200_OK)
        else:
            # Se falha na autenticação, retorna erro
            return Response({
                "detail": "Invalid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)

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

class VeiculoListCreateView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

    def perform_create(self, serializer):
        veiculo = serializer.save()
        # Atualiza no Firebase
        db.collection('veiculos').document(str(veiculo.id)).set({
            "placa": veiculo.placa,
            "modelo": veiculo.modelo,
            "marca": veiculo.marca,
            "cor": veiculo.cor,
        })

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

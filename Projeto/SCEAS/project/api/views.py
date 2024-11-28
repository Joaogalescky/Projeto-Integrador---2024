from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Usuario, Veiculo
from .serializers import UserSerializer, UsuarioSerializer, VeiculoSerializer
from firebase_config import db

# Criação de usuários (registro)
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Permite acesso público

    def perform_create(self, serializer):
        user = serializer.save()  # Salva o usuário no banco de dados
        token, created = Token.objects.get_or_create(user=user)  # Cria o token para o novo usuário

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

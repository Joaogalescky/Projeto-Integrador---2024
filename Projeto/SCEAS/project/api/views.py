from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from firebase_config import db
from .models import Usuario, Veiculo
from .serializers import UsuarioSerializer, VeiculoSerializer
from rest_framework import generics

# Página inicial (apenas para usuários autenticados)
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

# Função de login que renderiza a página
def login_view(request):
    # Renderiza a página de login se o método não for POST
    return render(request, 'login.html')

# Função de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Endpoint de autenticação para o AJAX do frontend
@csrf_exempt  # Desativar CSRF apenas para fins de teste; melhore a segurança para produção
def api_login(request):
    if request.method == "POST":
        try:
            # Lê o corpo da requisição JSON
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Tentar autenticar com Django
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Faz o login e retorna resposta JSON de sucesso
                login(request, user)
                return JsonResponse({"success": True, "message": "Login realizado com sucesso"})
            else:
                # Credenciais inválidas
                return JsonResponse({"success": False, "message": "Credenciais inválidas"})
        except json.JSONDecodeError:
            # Erro no formato JSON da requisição
            return JsonResponse({"success": False, "message": "Erro na requisição. Verifique os dados enviados."})
    
    # Método não permitido
    return JsonResponse({"error": "Método não permitido"}, status=405)

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

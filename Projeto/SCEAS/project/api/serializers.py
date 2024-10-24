from rest_framework import serializers
from .models import Usuario, Veiculo

# Serializador de Veiculo
class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['id', 'placa', 'modelo', 'marca', 'cor']

# Serializador de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    veiculos = VeiculoSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'telefone', 'email', 'veiculos']
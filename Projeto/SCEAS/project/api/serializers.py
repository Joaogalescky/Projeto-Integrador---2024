from django.contrib.auth.models import User
from rest_framework import serializers
from firebase_config import db
from .models import Usuario, Veiculo

# Token
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 

    def create(self, validated_data):
        # Cria usuário com o método 'create_user' para garantir o hash da senha
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get['email', ''],
            password=validated_data['password']
        )
        return user

# Serializador de Veiculo
class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['id', 'placa', 'modelo', 'marca', 'cor']

# Serializador de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    veiculos = VeiculoSerializer(many=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'telefone', 'email', 'veiculos']

    # Create aninhado com o veiculo
    def create(self, validated_data):
        veiculos_data = validated_data.pop('veiculos')
        usuario = Usuario.objects.create(**validated_data)
        for veiculo_data in veiculos_data:
            Veiculo.objects.create(usuario=usuario, **veiculo_data)
        return usuario

    def update(self, instance, validated_data):
        veiculos_data = validated_data.pop('veiculos', None)
        instance.nome = validated_data.get('nome', instance.nome)
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if veiculos_data is not None:
            instance.veiculos.all().delete()  # Exclui os veículos antigos
            for veiculo_data in veiculos_data:
                Veiculo.objects.create(usuario=instance, **veiculo_data)
        return instance

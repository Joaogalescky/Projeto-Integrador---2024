from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    telefone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True, null=True)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='veiculos')
    placa = models.CharField(max_length=15, unique=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    cor = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.modelo} ({self.placa})'
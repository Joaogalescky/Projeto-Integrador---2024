from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
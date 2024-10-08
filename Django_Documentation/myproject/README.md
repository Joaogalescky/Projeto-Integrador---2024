# Projeto: Djando - Documentação

# Sobre o projeto
Arquivo de apresentação sobre a documentação para Django Rest Framework para a matéria de Projeto Integrador II - 2° TADS - Tecnólogo em Análise e Desenvolvimento de Sistemas | 2024.

## Índice
- [Introdução](#introdução)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Exemplo de Uso](#exemplo-de-uso)
- [Referências](#referencias)

## Requisitos
- Python
- Pacato Django e Django Rest Framework
- Pip (gerenciador de pacotes do Python)
- IDE (Visual Studio Code)
- Navegador (Chrome, Firefox, etc.)

## 1. Preparando projeto

### 1.1 Selecionando local do projeto
Abra um terminal bash em sua Área de Trabalho
```bash
cd Desktop
ou
cd Área\ de\ Trabalho/
```

### 1.2 Criação e utilização da pasta do projeto
```bash
mkdir DjangoDocumentacao
```
```bash
cd DjangoDocumentacao
```

## 2. Construindo o projeto
### 2.1  Django e Django Rest Framework
#### 2.1.1 Instação do pacote
```bash
pip install django djangorestframework
```

#### 2.1.2 Criação do projeto Django
```bash
django-admin startproject projeto
cd projeto
```
#### 2.1.3 Editando os settings.py
```bash
INSTALLED_APPS = [
    'api',
    'rest_framework',
    ...
]
```

#### 2.1.4 Incluindo as urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

#### 2.1.5 Criação da API Django
```bash
cd ..
python manage.py startapp api
cd api/
```

#### 2.1.6 Definindo o models.py
```bash
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
```

#### 2.1.7 Executar as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.1.8 Criar serializers
```bash
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']
```

#### 2.1.9 Criar Views
```bash
# api/views.py
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

#### 2.2.0 Configurar URLs
```bash
# api/urls.py
from django.urls import path
from .views import ItemListCreate, ItemDetail

urlpatterns = [
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]
```

### 3. Testar a API
```bash
python manage.py runserver
```
```bash
GET /api/items/ – Lista todos os itens.
POST /api/items/ – Cria um novo item.
GET /api/items/<id>/ – Retorna detalhes de um item específico.
```

#### 3.1 Exemplos de requisições:
* GET para listar todos os itens:
```bash
curl http://127.0.0.1:8000/api/items/
```

* POST para criar um novo item:
```bash
curl -X POST http://127.0.0.1:8000/api/items/ -d '{"name": "Item 1", "description": "Descrição do item 1"}' -H "Content-Type: application/json"
```

#### 4. Endpoints da API
## Propostas
Cadastro de Items: 
```
POST /api/items/
```
Edição de Items: 
```
PUT /api/items/
```
Deletar Items: 
```
DELETE /api/items/
```
Buscar Items: 
```
GET /api/items/{id}/
```
- Corpo de requisição (JSON):
```bash
{
    "name": "Nome do Item",
    "description": "Descrição do Item"
}
```

## Estrutura do Arquivo
```bash
DjangoDocumentacao/
│
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── projeto/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
```

# Autor

João Vitor Campõe Galescky

# Referência

https://www.youtube.com/watch?v=4u0aI-90KnU&ab_channel=HashtagPrograma%C3%A7%C3%A3o

https://www.youtube.com/watch?v=rwSHQqQWGnI&list=PLZ5WLsqE1WPGPA0Z0H1XB8P6UwgTHOSaf&ab_channel=TreinaWeb

## IFPR

[![IFPR Logo](https://user-images.githubusercontent.com/126702799/234438114-4db30796-20ad-4bec-b118-246ebbe9de63.png)](https://user-images.githubusercontent.com/126702799/234438114-4db30796-20ad-4bec-b118-246ebbe9de63.png)

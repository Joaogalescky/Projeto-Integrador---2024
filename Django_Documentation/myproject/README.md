# Projeto: Djando - Documentação
 
Arquivo de apresentação sobre a documentação para Django Rest Framework para a matéria de Projeto Integrador II - 2° TADS - Tecnólogo em Análise e Desenvolvimento de Sistemas | 2024.

## Índice
- [Introdução](#1-introdução)
- [Requisitos](#2-requisitos)
- [Preparando](#3-preparando-projeto)
- [Construindo](#4-construindo-o-projeto)
- [Testando](#5-testar-a-api)
- [Estrutura do Arquivo](#6-estrutura-do-arquivo)
- [Referências](#referências)

## 1. Introdução

O Swagger

## 2. Requisitos
- Python
- Pacato Django e Django Rest Framework
- Pip (gerenciador de pacotes do Python)
- IDE (Visual Studio Code)
- Navegador (Chrome, Firefox, etc.)

## 3. Preparando projeto

### 3.1 Selecionando local do projeto
Abra um terminal bash em sua Área de Trabalho
```bash
cd Desktop
ou
cd Área\ de\ Trabalho/
```

### 3.2 Criação e utilização da pasta do projeto
```bash
mkdir DjangoDocumentacao
```
```bash
cd DjangoDocumentacao
```

## 4. Construindo o projeto
### 4.1  Django, Django Rest Framework e Swagger
#### 4.1.1 Instação do pacote
```bash
pip install django djangorestframework drf-yasg
```

#### 4.1.2 Criação do projeto Django
```bash
django-admin startproject projeto
cd projeto
```
#### 4.1.3 Editando os settings.py
```bash
INSTALLED_APPS = [
    'api',
    'rest_framework',
    ...
]
```

#### 4.1.4 Incluindo as urls.py
```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

#### 4.1.5 Criação da API Django
```bash
cd ..
python manage.py startapp api
cd api/
```

#### 4.1.6 Definindo o models.py
```bash
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
```

#### 4.1.7 Executar as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4.1.8 Criar serializers
```bash
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']
```

#### 4.1.9 Criar Views
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

#### 4.2.0 Configurar URLs
```bash
# api/urls.py
from django.urls import path
from .views import ItemListCreate, ItemDetail

urlpatterns = [
    path('items/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]
```

### 5. Testar a API
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

#### 3.2 Endpoints da API
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

## 6. Estrutura do Arquivo
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

# Referências

HASHTAG PROGRAMAÇÃO. Django framework: do zero até o deploy [YouTube]. 16 fev. 2021. Disponível em: https://www.youtube.com/watch?v=4u0aI-90KnU&ab_channel=HashtagPrograma%C3%A7%C3%A3o. Acesso em: 8 out. 2024.

TREINA WEB. Desenvolvimento web com Django: fundamentos e boas práticas [YouTube]. 13 jun. 2020. Disponível em: https://www.youtube.com/watch?v=rwSHQqQWGnI&list=PLZ5WLsqE1WPGPA0Z0H1XB8P6UwgTHOSaf&ab_channel=TreinaWeb. Acesso em: 8 out. 2024.

CÓDIGO FONTE TV. Como funciona o Django framework: explicação prática [YouTube]. 10 ago. 2021. Disponível em: https://www.youtube.com/watch?v=3nl9AzttzBQ&ab_channel=C%C3%B3digoFonteTV. Acesso em: 8 out. 2024.

DJANGOROAD. Django para iniciantes: introdução e primeiros passos [YouTube]. 5 set. 2019. Disponível em: https://www.youtube.com/watch?v=JC6gHKeegk4&ab_channel=Djangoroad. Acesso em: 8 out. 2024.

BRAINTEMPLE TUTORIAL TV. Aplicações web com Django: passo a passo completo [YouTube]. 22 nov. 2020. Disponível em: https://www.youtube.com/watch?v=7MS1Z_1c5CU&list=PLnBvgoOXZNCOiV54qjDOPA9R7DIDazxBA&ab_channel=BraintempleTutorialTV. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Tutorial – Parte 1. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/intro/tutorial01/. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Conteúdos e Referências. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/contents/. Acesso em: 8 out. 2024.

DJANGO REST SWAGGER. Django REST Swagger: Documentação. Disponível em: https://django-rest-swagger.readthedocs.io/en/latest/. Acesso em: 8 out. 2024.

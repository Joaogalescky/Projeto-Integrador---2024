﻿# Projeto: Djando - Documentação
 
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

O Swagger é um conjunto de ferramentas open source que visa facilitar para os  desenvolvedores na modelagem, documentação e teste de API's em seus processos: definição, criação, documentação e consumo de APIs REST (como endpoints, dados recebidos, dados retornados, códigos HTTP, métodos de autenticação etc). Permitindo que tanto humanos quanto máquinas compreendam suas funcionalidades sem acesso direto ao código-fonte.

Se destaca por:
* Padronização: Swagger permite a descrição dos recursos de uma API, como endpoints, parâmetros, tipos de dados e códigos HTTP;
* Documentação Automática: Gera documentação legível e interativa, facilitando o entendimento e a integração com outras aplicações;
* Testes: Possui uma interface que permite testar endpoints diretamente na documentação, melhorando a usabilidade.

Inclui várias ferramentas:
* Swagger UI: Interface gráfica que exibe a documentação da API e permite interagir com seus endpoints;
* Swagger Editor: Um editor online que permite criar definições de API usando formatos como YAML ou JSON;
* Swagger Codegen: Gera código cliente e servidor em várias linguagens, facilitando a implementação.

## 2. Requisitos
- Python
- Pacato Django, Django Rest Framework, Swagger
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
#### 4.1.1 Instação dos pacotes
```bash
pip install django djangorestframework
pip install django-rest-swagger
pip install pyyaml
pip install inflection
```

#### 4.1.2 Criação do projeto Django
```bash
django-admin startproject projeto
cd projeto
```

#### 4.1.3 Criação da API Django
```bash
python manage.py startapp api
```

#### 4.1.4 Editar os settings.py
```bash
import os

[...]

INSTALLED_APPS = [
    'api',
    'rest_framework',
    'rest_framework_swagger',
    [...]
]

[...]

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        [...]
    },
]
```

#### 4.1.5 Definir o models.py
```bash
#api/models.py
from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
```

#### 4.1.6 Criar serializers na pasta 'api'
```bash
#api/serializers.py
from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'idade', 'email', 'curso']
```

#### 4.1.7 Definir Views
```bash
# api/views.py
from django.shortcuts import render
from rest_framework import viewsets
from .models import Aluno
from .serializers import AlunoSerializer

# Create your views here.
class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
```

#### 4.1.8 Incluir as urls.py
```bash
#projeto/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api_schema', get_schema_view(title='Documentação API', description='Descrição para o guia de documentação Django REST API'), name='api_schema'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swagger/', TemplateView.as_view(
            template_name='swagger.html',
            extra_context={'schema_url':'api_schema'}
        ), 
    name='swagger-ui'),
]
```

#### 4.1.9 Criar URLs na pasta 'api'
```bash
# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet, basename='aluno')

urlpatterns = router.urls
```

#### 4.2.0 Criar template do swagger
```bash
# DjangoDocumentacao/projeto
mkdir templates
cd templates
touch swagger.html
```
```bash
<!DOCTYPE html>
<html>
  <head>
    <title>School Service Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
        url: "{% url schema_url %}",
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      })
    </script>
  </body>
</html>
```

#### 4.2.1 Executar as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Testar a API
```bash
python manage.py runserver
```
```bash
http://127.0.0.1:8000/swagger/
```

#### 5.1 Endpoints da API
Cadastro Alunos: 
```
POST /api/alunos/
```
Buscar Alunos: 
```
GET /api/alunos/{id}/
```
Listar Alunos: 
```
GET /api/alunos/{id}/
```
Atualizar Alunos: 
```
PUT /api/alunos/
```
Atualizar Alunos: 
```
PUT /api/alunos/
```
Deletar Alunos: 
```
DELETE /api/alunos/
```

- Corpo de requisição (JSON):
```bash
{
  "nome": "string",
  "idade": 0,
  "email": "user@example.com",
  "curso": "string"
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

BRAINTEMPLE TUTORIAL TV. Aplicações web com Django: passo a passo completo [YouTube]. 22 nov. 2020. Disponível em: https://www.youtube.com/watch?v=7MS1Z_1c5CU&list=PLnBvgoOXZNCOiV54qjDOPA9R7DIDazxBA&ab_channel=BraintempleTutorialTV. Acesso em: 8 out. 2024.

CÓDIGO FONTE TV. Como funciona o Django framework: explicação prática [YouTube]. 10 ago. 2021. Disponível em: https://www.youtube.com/watch?v=3nl9AzttzBQ&ab_channel=C%C3%B3digoFonteTV. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Tutorial – Parte 1. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/intro/tutorial01/. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Conteúdos e Referências. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/contents/. Acesso em: 8 out. 2024.

DJANGO REST SWAGGER. Django REST Swagger: Documentação. Disponível em: https://django-rest-swagger.readthedocs.io/en/latest/. Acesso em: 8 out. 2024.

DJANGOROAD. Django para iniciantes: introdução e primeiros passos [YouTube]. 5 set. 2019. Disponível em: https://www.youtube.com/watch?v=JC6gHKeegk4&ab_channel=Djangoroad. Acesso em: 8 out. 2024.

GR1D. Swagger: entenda o que é e como usar. Disponível em: https://gr1d.io/2022/04/15/swagger/. Acesso em: 9. out. 2024.

HASHTAG PROGRAMAÇÃO. Django framework: do zero até o deploy [YouTube]. 16 fev. 2021. Disponível em: https://www.youtube.com/watch?v=4u0aI-90KnU&ab_channel=HashtagPrograma%C3%A7%C3%A3o. Acesso em: 8 out. 2024.

TREINA WEB. Desenvolvimento web com Django: fundamentos e boas práticas [YouTube]. 13 jun. 2020. Disponível em: https://www.youtube.com/watch?v=rwSHQqQWGnI&list=PLZ5WLsqE1WPGPA0Z0H1XB8P6UwgTHOSaf&ab_channel=TreinaWeb. Acesso em: 8 out. 2024.

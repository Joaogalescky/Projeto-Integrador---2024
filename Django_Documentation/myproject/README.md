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

O Swagger é um conjunto de ferramentas open source que visa facilitar para os desenvolvedores na modelagem, documentação e teste de API's em seus processos: definição, criação, documentação e consumo de APIs REST (como endpoints, dados recebidos, dados retornados, códigos HTTP, métodos de autenticação etc). Permitindo que tanto humanos quanto máquinas compreendam suas funcionalidades sem acesso direto ao código-fonte.

Se destaca por:
* Padronização: Swagger permite a descrição dos recursos de uma API, como endpoints, parâmetros, tipos de dados e códigos HTTP;
* Documentação Automática: Gera documentação legível e interativa, facilitando o entendimento e a integração com outras aplicações;
* Testes: Possui uma interface que permite testar endpoints diretamente na documentação, melhorando a usabilidade.

Inclui várias ferramentas:
* Swagger UI: Interface gráfica que exibe a documentação da API e permite interagir com seus endpoints;
* Swagger Editor: Um editor online que permite criar definições de API usando formatos como YAML ou JSON;
* Swagger Codegen: Gera código cliente e servidor em várias linguagens, facilitando a implementação.

O drf-yasg (Django Rest Framework - Yet Another Swagger Generator) é uma biblioteca para o Django Rest Framework que gera automaticamente a documentação Swagger/OpenAPI da sua API. Essa documentação descreve os endpoints, os métodos HTTP suportados (GET, POST, PUT, DELETE, etc.), e como interagir com eles, fornecendo uma interface visual interativa (via Swagger UI), onde você pode testar os endpoints diretamente no navegador.

Características:
* Geração Automática de Documentação: inspeciona os serializers, viewsets e rotas definidos na sua API para gerar a documentação automaticamente;
* Suporte ao OpenAPI/Swagger;
* Interface Interativa via Swagger;
* Personalização: oferece uma série de opções para personalizar a aparência e a forma como a documentação é gerada, como customizar títulos, descrições e campos adicionais.

O ReDoc é uma outra interface gráfica de documentação de APIs OpenAPI, assim como o Swagger UI, mas com algumas diferenças em estilo e funcionalidade. É conhecido por ser muito mais moderno, minimalista e otimizado para uma melhor usabilidade em comparação com o Swagger UI, estando focado em uma melhor legibilidade e na organização da documentação, especialmente para APIs maiores e mais complexas.

Características principais do ReDoc:
* Design limpo e organizado: oferece uma interface mais elegante e moderna, com foco na apresentação organizada de informações, especialmente em APIs grandes;
* Divisão de Seções: agrupa automaticamente a documentação em seções, facilitando a navegação;
* Melhor legibilidade: focado na leitura e na compreensão de como os endpoints funcionam;
* Suporte total ao OpenAPI.

## 2. Requisitos
- Python
- Pacote Django, Django Rest Framework, D
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
### 4.1  Django, Django Rest Framework e drf-yasg
#### 4.1.1 Instação do pacote
```bash
pip install django djangorestframework
pip install drf-yasg
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
INSTALLED_APPS = [
    'api',
    'drf_yasg'
    'rest_framework',
    ...
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do esquema da API
schema_view = get_schema_view(
    openapi.Info(
        title="Minha API",
        default_version='v1',
        description="Descrição do projeto de exemplo",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@minhaapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Inclua suas URLs da API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Interface do Swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Interface do ReDoc
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

#### 4.2.0 Executar as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Testar a API
```bash
python manage.py runserver
```
```bash
#Swagger UI
http://127.0.0.1:8000/swagger/
#ReDoc 
http://127.0.0.1:8000/redoc/
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

HASHTAG PROGRAMAÇÃO. Django framework: do zero até o deploy [YouTube]. 16 fev. 2021. Disponível em: https://www.youtube.com/watch?v=4u0aI-90KnU&ab_channel=HashtagPrograma%C3%A7%C3%A3o. Acesso em: 8 out. 2024.

TREINA WEB. Desenvolvimento web com Django: fundamentos e boas práticas [YouTube]. 13 jun. 2020. Disponível em: https://www.youtube.com/watch?v=rwSHQqQWGnI&list=PLZ5WLsqE1WPGPA0Z0H1XB8P6UwgTHOSaf&ab_channel=TreinaWeb. Acesso em: 8 out. 2024.

CÓDIGO FONTE TV. Como funciona o Django framework: explicação prática [YouTube]. 10 ago. 2021. Disponível em: https://www.youtube.com/watch?v=3nl9AzttzBQ&ab_channel=C%C3%B3digoFonteTV. Acesso em: 8 out. 2024.

DJANGOROAD. Django para iniciantes: introdução e primeiros passos [YouTube]. 5 set. 2019. Disponível em: https://www.youtube.com/watch?v=JC6gHKeegk4&ab_channel=Djangoroad. Acesso em: 8 out. 2024.

BRAINTEMPLE TUTORIAL TV. Aplicações web com Django: passo a passo completo [YouTube]. 22 nov. 2020. Disponível em: https://www.youtube.com/watch?v=7MS1Z_1c5CU&list=PLnBvgoOXZNCOiV54qjDOPA9R7DIDazxBA&ab_channel=BraintempleTutorialTV. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Tutorial – Parte 1. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/intro/tutorial01/. Acesso em: 8 out. 2024.

DJANGO SOFTWARE FOUNDATION. Django: Conteúdos e Referências. 2024. Disponível em: https://docs.djangoproject.com/pt-br/5.1/contents/. Acesso em: 8 out. 2024.

DJANGO REST SWAGGER. Django REST Swagger: Documentação. Disponível em: https://django-rest-swagger.readthedocs.io/en/latest/. Acesso em: 8 out. 2024.

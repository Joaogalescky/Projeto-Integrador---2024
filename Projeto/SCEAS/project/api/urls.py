from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterAPIView, UsuarioListCreateView, UsuarioUpdateDeleteView, VeiculoListCreateView, VeiculoUpdateDeleteView

urlpatterns = [
    # Registro
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),

    # Login (token)
    path('auth/', obtain_auth_token, name='api_token_auth'),

    # Páginas Web
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    
    # Endpoints para usuários
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioUpdateDeleteView.as_view(), name='usuario-detail'),
    
    # Endpoints para veículos
    path('veiculos/', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('veiculos/<int:pk>/', VeiculoUpdateDeleteView.as_view(), name='veiculo-detail'),
]
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterAPIView, UserLoginAPIView, UsuarioListCreateView, UsuarioUpdateDeleteView, VeiculoListCreateView, VeiculoUpdateDeleteView

urlpatterns = [
    #Token
    path('auth/', obtain_auth_token, name='api_token_auth'),
    
    # Registro de usuário
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),

    # Login (Token de autenticação via POST)
    path('login/', UserLoginAPIView.as_view(), name='user-login'),

    # Páginas Web
    path('home/', views.home, name='home'),
    path('cadastre/', views.register_view, name='cadastre'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.login_view, name='entry'),
    # path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    
    # Endpoints para usuários
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioUpdateDeleteView.as_view(), name='usuario-detail'),
    
    # Endpoints para veículos
    path('veiculos/', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('veiculos/<int:pk>/', VeiculoUpdateDeleteView.as_view(), name='veiculo-detail'),
]
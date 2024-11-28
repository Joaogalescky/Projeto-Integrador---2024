from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterAPIView, UserLoginAPIView, UsuarioListCreateView, UsuarioUpdateDeleteView, VeiculoListCreateView, VeiculoUpdateDeleteView

urlpatterns = [
    # Registro de usuário
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),

    # Login (Token de autenticação via POST)
    path('login/', UserLoginAPIView.as_view(), name='user-login'),

    # Páginas Web
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Endpoints para usuários
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioUpdateDeleteView.as_view(), name='usuario-detail'),
    
    # Endpoints para veículos
    path('veiculos/', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('veiculos/<int:pk>/', VeiculoUpdateDeleteView.as_view(), name='veiculo-detail'),
]
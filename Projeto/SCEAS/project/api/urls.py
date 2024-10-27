from django.urls import path
from .views import UsuarioListCreateView, UsuarioUpdateDeleteView, VeiculoListCreateView, VeiculoUpdateDeleteView

urlpatterns = [
    # Endpoints para usuários
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioUpdateDeleteView.as_view(), name='usuario-detail'),
    
    # Endpoints para veículos
    path('veiculos/', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('veiculos/<int:pk>/', VeiculoUpdateDeleteView.as_view(), name='veiculo-detail'),
]
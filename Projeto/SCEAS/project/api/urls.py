from django.urls import path
from .views import UsuarioListCreateView, UsuarioDetailView, VeiculoListCreateView, VeiculoDetailView

urlpatterns = [
    # Endpoints para usuários
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<int:pk>/', UsuarioDetailView.as_view(), name='usuario-detail'),
    
    # Endpoints para veículos
    path('veiculos/', VeiculoListCreateView.as_view(), name='veiculo-list-create'),
    path('veiculos/<int:pk>/', VeiculoDetailView.as_view(), name='veiculo-detail'),
]
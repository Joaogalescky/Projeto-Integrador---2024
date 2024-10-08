from django.urls import path
from .views import ItemListCreate, ItemDetail

urlpatters = [
    path('item/', ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]
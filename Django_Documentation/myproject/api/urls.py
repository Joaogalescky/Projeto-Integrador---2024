from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'itens', ItemViewSet, basename='item')

urlpatterns = router.urls
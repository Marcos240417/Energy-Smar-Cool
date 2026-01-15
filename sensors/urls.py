from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, LojaViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'lojas', LojaViewSet, basename='loja') # Nova rota adicionada

urlpatterns = [
    path('', include(router.urls)),
]
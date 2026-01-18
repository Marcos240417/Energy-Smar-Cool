from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensor')

urlpatterns = [
    path('', include(router.urls)),
]


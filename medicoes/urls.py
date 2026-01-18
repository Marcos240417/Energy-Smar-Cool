from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicaoViewSet

router = DefaultRouter()
router.register(r'', MedicaoViewSet, basename='medicao')

urlpatterns = [
    path('', include(router.urls)),
]
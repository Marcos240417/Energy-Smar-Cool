from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from sensors.views import SensorViewSet, LojaViewSet 

router = DefaultRouter()
router.register(r"lojas", LojaViewSet, basename="loja")
router.register(r"sensors", SensorViewSet, basename="sensor")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Rotas de Autenticação JWT
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
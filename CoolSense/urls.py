from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet, LojaViewSet, AparelhoViewSet
from alertas.views import AlertaViewSet
from medicoes.views import MedicaoViewSet  # se já criou
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"lojas", LojaViewSet, basename="loja")
router.register(r"aparelhos", AparelhoViewSet, basename="aparelho")
router.register(r"alertas", AlertaViewSet, basename="alerta")
router.register(r"medicoes", MedicaoViewSet, basename="medicao")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
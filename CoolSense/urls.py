from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Importações de Views
from core.views import UserViewSet, LojaViewSet, AparelhoViewSet
from alertas.views import AlertaViewSet
from medicoes.views import MedicaoViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"lojas", LojaViewSet, basename="loja")
router.register(r"aparelhos", AparelhoViewSet, basename="aparelho")
router.register(r"alertas", AlertaViewSet, basename="alerta")
router.register(r"medicoes", MedicaoViewSet, basename="medicao")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # Autenticação JWT
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Documentação Automática
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
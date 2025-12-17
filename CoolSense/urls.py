from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import UserViewSet, LojaViewSet, AparelhoViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"lojas", LojaViewSet, basename="loja")
router.register(r"aparelhos", AparelhoViewSet, basename="aparelho")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

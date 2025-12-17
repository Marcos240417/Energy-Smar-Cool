from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission

from .models import Loja, Aparelho
from .serializers import AparelhoSerializer
from .permissions import IsAdminOrTecnico
from rest_framework.serializers import ModelSerializer

# ======================================================
# PERMISSÕES (RBAC)
# ======================================================

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsTecnico(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "TECNICO"
        )


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "CLIENTE"
        )

# ======================================================
# SERIALIZERS
# ======================================================

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "loja",
            "tecnico_autorizado",
            "is_active",
        ]


class LojaSerializer(ModelSerializer):
    class Meta:
        model = Loja
        fields = "__all__"

# ======================================================
# VIEWSETS
# ======================================================

class UserViewSet(ModelViewSet):
    """
    CRUD de usuários.
    Acesso exclusivo do ADMIN.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class LojaViewSet(ModelViewSet):
    """
    CRUD de lojas.

    ADMIN   → acesso total
    TECNICO → leitura de lojas ativas
    CLIENTE → apenas sua própria loja
    """
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [IsAdmin() | IsTecnico() | IsCliente()]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Loja.objects.all()

        if user.role == "TECNICO":
            return Loja.objects.filter(ativa=True)

        if user.role == "CLIENTE":
            return Loja.objects.filter(id=user.loja_id)

        return Loja.objects.none()

# ======================================================
# REGRA DE NEGÓCIO
# ======================================================

def pode_ver_loja(user, loja_id) -> bool:
    if user.role == "ADMIN":
        return True

    if user.role == "TECNICO":
        return user.tecnico_autorizado

    if user.role == "CLIENTE":
        return user.loja_id == loja_id

    return False

# ======================================================
# APARELHOS (CRUD PRONTO)
# ======================================================

class AparelhoViewSet(ModelViewSet):
    """
    CRUD de aparelhos.

    ADMIN   → acesso total
    TECNICO → acesso total
    CLIENTE → leitura apenas da própria loja
    """
    queryset = Aparelho.objects.all()   # 🔥 ESSENCIAL
    serializer_class = AparelhoSerializer
    permission_classes = [IsAdminOrTecnico]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["ADMIN", "TECNICO"]:
            return Aparelho.objects.all()

        return Aparelho.objects.filter(loja=user.loja)

from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission

from .models import Loja, Aparelho
from .serializers import AparelhoSerializer
from .permissions import IsAdminOrTecnico, IsAdminOrTecnicoOrReadOnlyForCliente
from rest_framework.serializers import ModelSerializer


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



class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class LojaViewSet(ModelViewSet):

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
            if getattr(user, "tecnico_autorizado", False) and user.loja_id:
                return Loja.objects.filter(id=user.loja_id)
            return Loja.objects.none()

        if user.role == "CLIENTE":
            return Loja.objects.filter(id=user.loja_id)

        return Loja.objects.none()



def pode_ver_loja(user, loja_id) -> bool:
    if user.role == "ADMIN":
        return True

    if user.role == "TECNICO":
        return user.tecnico_autorizado

    if user.role == "CLIENTE":
        return user.loja_id == loja_id

    return False



class AparelhoViewSet(ModelViewSet):

    queryset = Aparelho.objects.all()
    serializer_class = AparelhoSerializer
    permission_classes = [IsAdminOrTecnicoOrReadOnlyForCliente]

    def get_queryset(self):
        user = self.request.user

        # Admin sees everything
        if user.role == "ADMIN":
            return Aparelho.objects.all()

        # Tecnico sees devices belonging to their loja if authorized
        if user.role == "TECNICO":
            if getattr(user, "tecnico_autorizado", False) and user.loja_id:
                return Aparelho.objects.filter(loja_id=user.loja_id)
            return Aparelho.objects.none()

        # Cliente sees devices for their loja only
        if user.role == "CLIENTE" and user.loja_id:
            return Aparelho.objects.filter(loja_id=user.loja_id)

        return Aparelho.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Admin can create for any loja
        if user.role == "ADMIN":
            return serializer.save()

        # Tecnico can create only for their loja
        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            return serializer.save(loja_id=user.loja_id)

        # Cliente cannot create
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Você não tem permissão para criar aparelhos.")

    def perform_update(self, serializer):
        user = self.request.user
        # Admin can update
        if user.role == "ADMIN":
            return serializer.save()

        # Tecnico can update only devices in their loja
        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            instancia = serializer.instance
            if instancia.loja_id != user.loja_id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Você não pode modificar aparelho de outra loja.")
            return serializer.save()

        # Cliente cannot update
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("Você não tem permissão para editar aparelhos.")

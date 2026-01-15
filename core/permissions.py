from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsTecnicoAutorizado(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "TECNICO"
            and request.user.tecnico_autorizado
        )


class IsAdminOrTecnico(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == "ADMIN":
            return True

        if request.user.role == "TECNICO":
            return request.user.tecnico_autorizado

        return False


class IsAdminOrTecnicoOrReadOnlyForCliente(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == "ADMIN":
            return True

        if request.user.role == "TECNICO":
            return getattr(request.user, "tecnico_autorizado", False)

        if request.user.role == "CLIENTE":
            return request.method in SAFE_METHODS

        return False

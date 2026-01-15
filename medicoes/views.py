from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrTecnicoOrReadOnlyForCliente
from .models import Medicao
from .serializers import MedicaoSerializer
from rest_framework.exceptions import PermissionDenied


class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.all().order_by('-registrada_em')
    serializer_class = MedicaoSerializer
    permission_classes = [IsAdminOrTecnicoOrReadOnlyForCliente]
    def get_queryset(self):
        user = self.request.user

        # Admin sees all
        if user.role == "ADMIN":
            return Medicao.objects.all().order_by('-registrada_em')

        # Tecnico sees medicoes for aparelhos in their loja
        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            return Medicao.objects.filter(aparelho__loja_id=user.loja_id).order_by('-registrada_em')

        # Cliente sees medicoes for their loja
        if user.role == "CLIENTE" and user.loja_id:
            return Medicao.objects.filter(aparelho__loja_id=user.loja_id).order_by('-registrada_em')

        return Medicao.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        # Only ADMIN or authorized TECNICO can create measurements via API
        if user.role == "ADMIN":
            return serializer.save()

        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            # ensure aparelho belongs to the same loja
            aparelho = serializer.validated_data.get('aparelho')
            if aparelho.loja_id != user.loja_id:
                raise PermissionDenied("Você não pode criar medições para aparelho de outra loja.")
            return serializer.save()

        raise PermissionDenied("Você não tem permissão para criar medições.")

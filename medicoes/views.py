from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrTecnicoOrReadOnlyForCliente
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .models import Medicao
from .serializers import MedicaoSerializer
from .filters import MedicaoFilter


class MedicaoPagination(PageNumberPagination):
    page_size = 20


class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.all().order_by('-registrada_em')
    serializer_class = MedicaoSerializer

    # permissões
    permission_classes = [IsAdminOrTecnicoOrReadOnlyForCliente]

    # filtros e paginação
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicaoFilter
    pagination_class = MedicaoPagination

    def get_queryset(self):
        user = self.request.user

        # Admin vê tudo
        if user.role == "ADMIN":
            return Medicao.objects.all().order_by('-registrada_em')

        # Técnico vê medições da loja dele
        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            return Medicao.objects.filter(aparelho__loja_id=user.loja_id).order_by('-registrada_em')

        # Cliente vê medições da loja dele
        if user.role == "CLIENTE" and user.loja_id:
            return Medicao.objects.filter(aparelho__loja_id=user.loja_id).order_by('-registrada_em')

        return Medicao.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        # Apenas ADMIN ou TECNICO autorizado podem criar medições
        if user.role == "ADMIN":
            return serializer.save()

        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            aparelho = serializer.validated_data.get('aparelho')
            if aparelho.loja_id != user.loja_id:
                raise PermissionDenied("Você não pode criar medições para aparelho de outra loja.")
            return serializer.save()

        raise PermissionDenied("Você não tem permissão para criar medições.")

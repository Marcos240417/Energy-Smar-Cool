import csv
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework.serializers import ModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Loja, Aparelho
from .serializers import AparelhoSerializer
from .permissions import IsAdminOrTecnico

from alertas.models import Alerta
from medicoes.models import Medicao


# --- Classes de Permissão ---

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and getattr(request.user, 'role', None) == "ADMIN"
        )


class IsTecnico(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and getattr(request.user, 'role', None) == "TECNICO"
        )


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and getattr(request.user, 'role', None) == "CLIENTE"
        )


# --- Serializadores ---

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "role",
            "loja", "tecnico_autorizado", "is_active",
        ]


class LojaSerializer(ModelSerializer):
    class Meta:
        model = Loja
        fields = "__all__"


# --- ViewSets ---

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
        return [(IsAdmin | IsTecnico | IsCliente)()]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)

        if role == "ADMIN":
            return Loja.objects.all()
        if role == "TECNICO":
            return Loja.objects.filter(ativa=True)
        if role == "CLIENTE":
            return Loja.objects.filter(id=user.loja_id)
        return Loja.objects.none()

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """Resumo rápido do status da loja em tempo real via relacionamento."""
        loja = self.get_object()
        aparelhos = Aparelho.objects.filter(loja=loja)

        # Correção: Filtra alertas ativos vinculados aos aparelhos desta loja
        alertas_ativos = Alerta.objects.filter(
            aparelho__loja=loja,
            ativo=True
        ).count()

        return Response({
            "loja": loja.nome,
            "total_aparelhos": aparelhos.count(),
            "alertas_ativos": alertas_ativos,
            "status_geral": "CRÍTICO" if alertas_ativos > 0 else "NORMAL"
        })

    @action(detail=True, methods=['get'])
    def estatisticas(self, request, pk=None):
        """Ranking de aparelhos com mais problemas nos últimos 30 dias via relacionamento."""
        loja = self.get_object()
        há_30_dias = timezone.now() - timedelta(days=30)

        # Correção: Busca via ForeignKey (Alerta -> Aparelho -> Loja)
        ranking = Alerta.objects.filter(
            aparelho__loja=loja,
            criado_em__gte=há_30_dias
        ).values('titulo').annotate(
            total_falhas=Count('id')
        ).order_by('-total_falhas')

        return Response({
            "loja": loja.nome,
            "periodo": "Últimos 30 dias",
            "ranking_manutencao": list(ranking)
        })

    @action(detail=True, methods=['get'], url_path='exportar-csv')
    def exportar_csv(self, request, pk=None):
        loja = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="historico_{loja.nome}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Equipamento', 'Temperatura (°C)', 'Umidade (%)', 'Data e Hora'])

        medicoes = Medicao.objects.filter(aparelho__loja=loja).order_by('-registrada_em')

        for m in medicoes:
            writer.writerow([
                m.aparelho.nome,
                m.temperatura,
                m.umidade,
                m.registrada_em.strftime('%d/%m/%Y %H:%M:%S')
            ])

        return response


class AparelhoViewSet(ModelViewSet):
    queryset = Aparelho.objects.all()
    serializer_class = AparelhoSerializer
    permission_classes = [IsAdminOrTecnico]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)

        if role in ["ADMIN", "TECNICO"]:
            return Aparelho.objects.all()
        return Aparelho.objects.filter(loja=user.loja)
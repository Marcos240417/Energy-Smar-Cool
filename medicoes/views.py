from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from .models import Medicao
from .serializers import MedicaoSerializer
from core.models import Aparelho
from alertas.models import Alerta

class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.all().order_by('-registrada_em')
    serializer_class = MedicaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'aparelho': ['exact'],
        'temperatura': ['gte', 'lte'],
        'umidade': ['gte', 'lte'],
        'registrada_em': ['date', 'gte', 'lte'],
    }

    def _verificar_limites(self, aparelho, temperatura):
        """Analisa a temperatura e gera alertas automáticos."""
        if temperatura > aparelho.temp_max:
            Alerta.objects.get_or_create(
                aparelho=aparelho,
                titulo="Temperatura Elevada!",
                ativo=True,
                defaults={
                    'mensagem': f"O {aparelho.nome} atingiu {temperatura}°C. Limite máx: {aparelho.temp_max}°C",
                    'nivel': 'critical'
                }
            )
        elif temperatura < aparelho.temp_min:
            Alerta.objects.get_or_create(
                aparelho=aparelho,
                titulo="Temperatura Baixa!",
                ativo=True,
                defaults={
                    'mensagem': f"O {aparelho.nome} atingiu {temperatura}°C. Limite mín: {aparelho.temp_min}°C",
                    'nivel': 'warning'
                }
            )

    @extend_schema(summary="Criação manual de medição via Web")
    def create(self, request, *args, **kwargs):
        aparelho_id = request.data.get('aparelho')
        temp = request.data.get('temperatura')
        umid = request.data.get('umidade')

        try:
            aparelho = Aparelho.objects.get(id=aparelho_id)
            aparelho.ultima_comunicacao = timezone.now()
            aparelho.save()

            medicao = Medicao.objects.create(aparelho=aparelho, temperatura=temp, umidade=umid)
            self._verificar_limites(aparelho, float(temp))

            serializer = self.get_serializer(medicao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Aparelho.DoesNotExist:
            return Response({"error": "Aparelho não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Ingestão de dados (Hardware ESP32)",
        description="Recebe dados simplificados do sensor via MAC Address.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "mac": {"type": "string", "example": "AA:BB:CC:DD:EE:FF"},
                    "t": {"type": "number", "example": 25.4},
                    "u": {"type": "number", "example": 60.5}
                },
                "required": ["mac", "t"]
            }
        },
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=['post'], url_path='esp-ingest', authentication_classes=[], permission_classes=[])
    def ingestao_esp(self, request):
        mac = request.data.get('mac')
        temp = request.data.get('t')
        umid = request.data.get('u', 0)

        if not mac or temp is None:
            return Response({"error": "Dados incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            aparelho = Aparelho.objects.get(mac_address=mac)
            aparelho.ultima_comunicacao = timezone.now()
            aparelho.save()

            Medicao.objects.create(aparelho=aparelho, temperatura=temp, umidade=umid)
            self._verificar_limites(aparelho, float(temp))

            return Response({"status": "recebido"}, status=status.HTTP_200_OK)
        except Aparelho.DoesNotExist:
            return Response({"error": "Hardware não cadastrado"}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        summary="Dados formatados para gráficos Recharts/Chart.js",
        parameters=[
            OpenApiParameter("aparelho", OpenApiTypes.INT, OpenApiParameter.QUERY, description="ID do aparelho", required=True)
        ]
    )
    @action(detail=False, methods=['get'], url_path='historico-grafico')
    def historico_grafico(self, request):
        aparelho_id = request.query_params.get('aparelho')
        if not aparelho_id:
            return Response({"error": "ID do aparelho obrigatório"}, status=400)

        periodo = timezone.now() - timedelta(hours=24)
        medicoes = Medicao.objects.filter(aparelho_id=aparelho_id, registrada_em__gte=periodo).order_by('registrada_em')

        if not medicoes.exists():
            return Response({"error": "Nenhum dado encontrado"}, status=404)

        return Response({
            "labels": [m.registrada_em.strftime('%H:%M') for m in medicoes],
            "temperaturas": [m.temperatura for m in medicoes],
            "umidades": [m.umidade for m in medicoes],
            "aparelho_nome": medicoes.first().aparelho.nome
        })
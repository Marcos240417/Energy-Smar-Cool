from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta

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
        """Analisa a temperatura e gera alertas automáticos baseados nos limites do aparelho."""
        if temperatura > aparelho.temp_max:
            Alerta.objects.create(
                aparelho=aparelho,
                titulo="Temperatura Elevada!",
                mensagem=f"O {aparelho.nome} atingiu {temperatura}°C. Limite máx: {aparelho.temp_max}°C",
                nivel="critical",
                ativo=True
            )
        elif temperatura < aparelho.temp_min:
            Alerta.objects.create(
                aparelho=aparelho,
                titulo="Temperatura Baixa!",
                mensagem=f"O {aparelho.nome} atingiu {temperatura}°C. Limite mín: {aparelho.temp_min}°C",
                nivel="warning",
                ativo=True
            )

    def create(self, request, *args, **kwargs):
        """Criação via Dashboard Web."""
        aparelho_id = request.data.get('aparelho')
        temp = request.data.get('temperatura')
        umid = request.data.get('umidade')

        try:
            aparelho = Aparelho.objects.get(id=aparelho_id)

            # Atualiza o timestamp de comunicação
            aparelho.ultima_comunicacao = timezone.now()
            aparelho.save()

            medicao = Medicao.objects.create(aparelho=aparelho, temperatura=temp, umidade=umid)
            self._verificar_limites(aparelho, float(temp))

            serializer = self.get_serializer(medicao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Aparelho.DoesNotExist:
            return Response({"error": "Aparelho não encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='esp-ingest')
    def ingestao_esp(self, request):
        """Endpoint para recepção de dados do ESP32/ESP8266 via MAC Address."""
        mac = request.data.get('mac')
        temp = request.data.get('t')
        umid = request.data.get('u')

        if not mac or temp is None:
            return Response({"error": "Dados incompletos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            aparelho = Aparelho.objects.get(mac_address=mac)

            # Atualiza o status de atividade do hardware
            aparelho.ultima_comunicacao = timezone.now()
            aparelho.save()

            Medicao.objects.create(aparelho=aparelho, temperatura=temp, umidade=umid)
            self._verificar_limites(aparelho, float(temp))

            return Response({"status": "recebido e processado"}, status=status.HTTP_200_OK)
        except Aparelho.DoesNotExist:
            return Response({"error": "Hardware não cadastrado"}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path='historico-grafico')
    def historico_grafico(self, request):
        aparelho_id = request.query_params.get('aparelho')
        if not aparelho_id:
            return Response({"error": "ID do aparelho obrigatório"}, status=400)

        periodo = timezone.now() - timedelta(hours=24)
        medicoes = Medicao.objects.filter(aparelho_id=aparelho_id, registrada_em__gte=periodo).order_by('registrada_em')

        return Response({
            "labels": [m.registrada_em.strftime('%H:%M') for m in medicoes],
            "temperaturas": [m.temperatura for m in medicoes],
            "umidades": [m.umidade for m in medicoes],
            "aparelho_nome": medicoes.first().aparelho.nome if medicoes.exists() else "N/A"
        })
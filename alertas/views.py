from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Alerta, AlertaLog
from .serializers import AlertaSerializer


class AlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar alertas.
    Permite a listagem, filtragem e resolução de problemas com auditoria.
    """
    queryset = Alerta.objects.all().order_by('-criado_em')
    serializer_class = AlertaSerializer

    def get_queryset(self):
        """
        Permite filtrar alertas por status (ativo=true/false) via query params.
        Exemplo: /api/alertas/?ativo=true
        """
        queryset = super().get_queryset()
        ativo = self.request.query_params.get('ativo', None)
        if ativo is not None:
            return queryset.filter(ativo=(ativo.lower() == 'true'))
        return queryset

    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """
        Endpoint: POST /api/alertas/{id}/resolver/
        Marca o alerta como inativo e registra o log de auditoria com o usuário logado.
        """
        alerta = self.get_object()

        if not alerta.ativo:
            return Response(
                {"detail": "Este alerta já foi resolvido anteriormente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        comentario = request.data.get('comentario', 'Resolvido pelo usuário via sistema.')

        # 1. Atualiza o status do alerta
        alerta.ativo = False
        # Mantemos o histórico na mensagem para visualização rápida
        alerta.mensagem += f"\n\n--- RESOLUÇÃO ---\n{comentario}"
        alerta.save()

        # 2. Cria o Log de Auditoria detalhado
        AlertaLog.objects.create(
            alerta=alerta,
            usuario=request.user,  # Captura o usuário do Token JWT no Postman
            observacao=comentario
        )

        return Response(
            {
                "status": "Alerta encerrado com sucesso.",
                "alerta": alerta.titulo,
                "resolvido_por": request.user.username,
                "data_resolucao": alerta.criado_em
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        """
        Endpoint: GET /api/alertas/{id}/historico/
        Retorna a linha do tempo de quem interagiu com este alerta.
        """
        alerta = self.get_object()
        logs = alerta.logs.all().values(
            'usuario__username',
            'observacao',
            'data_hora'
        )
        return Response(logs, status=status.HTTP_200_OK)
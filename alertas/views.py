from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrTecnicoOrReadOnlyForCliente
from .models import Alerta
from .serializers import AlertaSerializer


class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.filter(ativo=True).order_by('-criado_em')
    serializer_class = AlertaSerializer
    permission_classes = [IsAdminOrTecnicoOrReadOnlyForCliente]

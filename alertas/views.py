from rest_framework import viewsets
from .models import Alerta
from .serializers import AlertaSerializer

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.filter(ativo=True).order_by('-criado_em')
    serializer_class = AlertaSerializer

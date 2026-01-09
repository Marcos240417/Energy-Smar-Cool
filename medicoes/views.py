from rest_framework import viewsets
from .models import Medicao
from .serializers import MedicaoSerializer

class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.all().order_by('-registrada_em')
    serializer_class = MedicaoSerializer

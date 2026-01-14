from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Medicao
from .serializers import MedicaoSerializer
from .filters import MedicaoFilter

class MedicaoPagination(PageNumberPagination):
    page_size = 20  

class MedicaoViewSet(viewsets.ModelViewSet):
    queryset = Medicao.objects.all().order_by('-registrada_em') 
    serializer_class = MedicaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicaoFilter
    pagination_class = MedicaoPagination

  


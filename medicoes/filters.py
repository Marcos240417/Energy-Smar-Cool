import django_filters
from .models import Medicao

class MedicaoFilter(django_filters.FilterSet):
    sensor_id = django_filters.CharFilter(field_name="aparelho_id")
    data_inicio = django_filters.DateTimeFilter(field_name="registrada_em", lookup_expr='gte')
    data_fim = django_filters.DateTimeFilter(field_name="registrada_em", lookup_expr='lte')

    class Meta:
        model = Medicao
        fields = ['sensor_id', 'data_inicio', 'data_fim']
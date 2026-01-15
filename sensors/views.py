from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import models
from .models import Sensor, Loja
from .serializers import SensorSerializer, SensorListSerializer, LojaSerializer


class LojaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar as Lojas.
    """
    queryset = Loja.objects.all()
    serializer_class = LojaSerializer
    permission_classes = [AllowAny]


class SensorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar os Sensores.
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [AllowAny] 
    lookup_field = 'code' 
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SensorListSerializer
        return SensorSerializer
    
    def get_queryset(self):
        queryset = Sensor.objects.all()
        
        # Filtro por Ativo/Inativo
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # ATUALIZADO: Filtro por loja_id (novo campo do Model)
        loja_id = self.request.query_params.get('loja_id', None)
        if loja_id:
            queryset = queryset.filter(loja_id=loja_id)
        
        # Busca por nome ou código
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | 
                models.Q(code__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def activate(self, request, code=None):
        """Ativa o sensor"""
        sensor = self.get_object()
        sensor.is_active = True
        sensor.save()
        serializer = self.get_serializer(sensor)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, code=None):
        """Desativa o sensor"""
        sensor = self.get_object()
        sensor.is_active = False
        sensor.save()
        serializer = self.get_serializer(sensor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Retorna apenas sensores ativos"""
        active_sensors = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_sensors, many=True)
        return Response(serializer.data)
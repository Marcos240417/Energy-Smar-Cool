from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrTecnicoOrReadOnlyForCliente
from django.db import models
from .models import Sensor
from .serializers import SensorSerializer, SensorListSerializer
from rest_framework.exceptions import PermissionDenied


class SensorViewSet(viewsets.ModelViewSet):
    
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdminOrTecnicoOrReadOnlyForCliente]
    lookup_field = 'code' 
    
    def get_serializer_class(self):
        
        if self.action == 'list':
            return SensorListSerializer
        return SensorSerializer
    
    def get_queryset(self):
        user = self.request.user

        # start from all and then scope by role
        if user.role == "ADMIN":
            queryset = Sensor.objects.all()
        elif user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            queryset = Sensor.objects.filter(store_id=user.loja_id)
        elif user.role == "CLIENTE" and user.loja_id:
            queryset = Sensor.objects.filter(store_id=user.loja_id)
        else:
            queryset = Sensor.objects.none()
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
       
        store_id = self.request.query_params.get('store_id', None)
        if store_id:
            # allow admins to filter other store ids, otherwise ensure it's within scoped queryset
            if user.role == "ADMIN":
                queryset = queryset.filter(store_id=store_id)
            else:
                queryset = queryset.filter(store_id=store_id)
        
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | 
                models.Q(code__icontains=search)
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def activate(self, request, code=None):
        """Activates a sensor"""
        sensor = self.get_object()
        sensor.is_active = True
        sensor.save()
        serializer = self.get_serializer(sensor)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, code=None):
        """Deactivates a sensor"""
        sensor = self.get_object()
        sensor.is_active = False
        sensor.save()
        serializer = self.get_serializer(sensor)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_sensors = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_sensors, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "ADMIN":
            return serializer.save()

        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            return serializer.save(store_id=user.loja_id)

        raise PermissionDenied("Você não tem permissão para criar sensores.")

    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "ADMIN":
            return serializer.save()

        if user.role == "TECNICO" and getattr(user, "tecnico_autorizado", False) and user.loja_id:
            instance = serializer.instance
            if instance.store_id != user.loja_id:
                    raise PermissionDenied("Você não pode modificar sensor de outra loja.")
            return serializer.save()

        raise PermissionDenied("Você não tem permissão para editar sensores.")


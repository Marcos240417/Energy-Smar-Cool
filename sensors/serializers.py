from rest_framework import serializers
from .models import Sensor, Loja

class LojaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Loja.
    """
    class Meta:
        model = Loja
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Sensor atualizado com Loja.
    """
    status_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Sensor
        fields = [
            'id',
            'name',
            'code',
            'description',
            'loja', # Alterado de store_id para loja
            'min_temperature',
            'max_temperature',
            'is_active',
            'device_type',
            'ip_address',
            'created_at',
            'updated_at',
            'status_display',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_code(self, value):
        if self.instance and self.instance.code == value:
            return value
        
        if Sensor.objects.filter(code=value).exists():
            raise serializers.ValidationError("A sensor with this code already exists.")
        return value
    
    def validate(self, data):
        # Busca os valores nos dados enviados ou no objeto existente se for um update
        temp_min = data.get('min_temperature', self.instance.min_temperature if self.instance else -10.0)
        temp_max = data.get('max_temperature', self.instance.max_temperature if self.instance else 10.0)
        
        if temp_min is not None and temp_max is not None and temp_min >= temp_max:
            raise serializers.ValidationError({
                'min_temperature': 'Minimum temperature must be less than maximum temperature.'
            })
        
        return data

class SensorListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listagem.
    """
    status_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Sensor
        fields = [
            'id',
            'name',
            'code',
            'loja', # Alterado de store_id para loja
            'is_active',
            'status_display',
            'created_at',
        ]
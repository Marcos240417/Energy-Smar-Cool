from rest_framework import serializers
from .models import Sensor


class SensorSerializer(serializers.ModelSerializer):

    status_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Sensor
        fields = [
            'id',
            'name',
            'code',
            'description',
            'store_id',
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
       
        temp_min = data.get('min_temperature', self.instance.min_temperature if self.instance else None)
        temp_max = data.get('max_temperature', self.instance.max_temperature if self.instance else None)
        
        if temp_min and temp_max and temp_min >= temp_max:
            raise serializers.ValidationError({
                'min_temperature': 'Minimum temperature must be less than maximum temperature.'
            })
        
        return data


class SensorListSerializer(serializers.ModelSerializer):
  
    status_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Sensor
        fields = [
            'id',
            'name',
            'code',
            'store_id',
            'is_active',
            'status_display',
            'created_at',
        ]



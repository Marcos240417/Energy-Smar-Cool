from rest_framework import serializers
from .models import Medicao

class MedicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicao
        fields = '__all__'

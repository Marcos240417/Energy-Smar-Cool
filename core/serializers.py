from rest_framework.serializers import ModelSerializer
from .models import Aparelho


class AparelhoSerializer(ModelSerializer):
    class Meta:
        model = Aparelho
        fields = "__all__"

from rest_framework import serializers
from .models import TWTestToken


class TWTestTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TWTestToken
        fields = ("__all__")
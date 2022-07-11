from rest_framework import serializers

from .models import Patient

from users.models import User
from users.serializers import UserSerializer, BasicUserSerializer

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        return response 

class BasicPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id',] 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = BasicUserSerializer(instance.user).data
        return response             
            

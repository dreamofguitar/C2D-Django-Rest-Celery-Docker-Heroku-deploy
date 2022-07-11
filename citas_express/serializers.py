from rest_framework import serializers 

from citas_express.models import CitaExpress 

from patients.serializers import BasicPatientSerializer

class CitaExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaExpress 
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = BasicPatientSerializer(instance.patient).data
        return response
        

class BasicCitaExpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaExpress 
        fields = ('id', 'patient', 'appointment_reason')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = BasicPatientSerializer(instance.patient).data
        return response
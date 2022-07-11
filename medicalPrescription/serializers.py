from rest_framework import serializers 

from .models import Prescription

from doctors.serializers import BasicDoctorSerializer
from patients.serializers import BasicPatientSerializer 


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription 
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = BasicPatientSerializer(instance.patient).data
        response['doctor'] = BasicDoctorSerializer(instance.doctor).data

        return response 

class DoctorPrescriptionSerializer(serializers.ModelSerializer):
    #patient = serializers.StringRelatedField(many=True)

    class Meta:
        model = Prescription
        fields = ('fecha', 'patient', 'appointment_type')

class PatientPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ('fecha', 'doctor', 'appointment_type')
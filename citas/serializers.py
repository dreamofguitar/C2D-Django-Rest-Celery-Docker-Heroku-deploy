from rest_framework import serializers 

from .models import Cita


from doctors.serializers import BasicDoctorSerializer
from patients.serializers import BasicPatientSerializer 


class CitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita 
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = BasicPatientSerializer(instance.patient).data
        response['doctor'] = BasicDoctorSerializer(instance.doctor).data

        return response 

class DoctorCitasSerializer(serializers.ModelSerializer):
    #patient = serializers.StringRelatedField(many=True)
    class Meta:
        model = Cita
        fields = ('id', 'date_time', 'patient', 'appointment_type', 'accept')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = BasicPatientSerializer(instance.patient).data

        return response 


class PatientCitasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cita
        fields = ('id', 'date_time', 'doctor', 'appointment_type', 'accept', 'completed')
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['doctor'] = BasicDoctorSerializer(instance.doctor).data
        
        return response
        
class BasicCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ('id', 'is_active', 'accept', 'room','completed')
class AcceptCitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ('accept', ) 
                
        
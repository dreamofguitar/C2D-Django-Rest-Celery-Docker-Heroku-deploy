from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 

from patients.serializers import BasicPatientSerializer 
from patients.models import Patient
from doctors.serializers import BasicDoctorSerializer 
from doctors.models import Doctor
from medicalPrescription.serializers import (PrescriptionSerializer, DoctorPrescriptionSerializer, PatientPrescriptionSerializer)
from medicalPrescription.permissions import IsOwner, IsPatient, IsDoctor 
from medicalPrescription.models import Prescription

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsDoctor])
def createPrescription(request):

    data = request.data 

    try:
        doctor = Doctor.objects.get(id=request.data['doctor'])
    except:
        return Response({'Error': 'No se econtro un doctor con ese id'})
    doctor_serializer = BasicDoctorSerializer(instance=doctor, data=data, partial=True) 
    doctor_serializer.is_valid()   

    prescription_serializer = PrescriptionSerializer(data=data, partial=True)
    prescription_serializer.is_valid(raise_exception=True)
    prescription_serializer.save()
    
    return Response(prescription_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def listPrescriptions(request):
    data =  Prescription.objects.get(id=id)
    serializer = PrescriptionSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listPrescription(request, id):
    prescription = Prescription.objects.get(id=id)
    serializer = PrescriptionSerializer(prescription, many=False, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsDoctor])
def docListPrescription(request, id_doctor):
    doctor = Doctor.objects.filter(id=id_doctor)
    prescription = Prescription.objects.filter(doctor__in=doctor)
    serializer = DoctorPrescriptionSerializer(prescription, many=True, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPatient])
def patListPrescription(request, id_patient):
    patient = Patient.objects.filter(id=id_patient)
    prescription = Prescription.objects.filter( patient__in=patient)    
    serializer = PatientPrescriptionSerializer(prescription, many=True, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsDoctor])
def deletePrescription(request, id):
    prescription = Prescription.objects.get(id=id)
    prescription.delete()

    return Response('Prescripcion Eliminada')
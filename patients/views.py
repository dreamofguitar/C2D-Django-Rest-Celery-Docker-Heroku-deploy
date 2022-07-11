from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

import requests

from patients.serializers import PatientSerializer
from patients.models import Patient

from citas.permissions import IsPatient

from users.serializers import UserSerializer

#En esta vista vista se registra el paciente 
@api_view(['POST'])
@permission_classes([AllowAny])
def patientCreate(request):
    '''
    Input should be in the format:
    {"email": "test4234@gmail.com", "password": "1234abcd", "patient_description": "A brief description of the patient", "name": "patientsname", "first_name": "Perez", "last_name": "Perez", "birthday": "25/04/2001", "phone": "123456789", "description": "Hello"}
    '''
    data = request.data
    user_serializer = UserSerializer(data=data, partial=True)
    user_serializer.is_valid()
    user_serializer.save()
    data['user'] = user_serializer.instance.id
    serializer = PatientSerializer(data=data, partial=True)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


#En esta vista se listan a TODOS los pacientes en la DB 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listAll(request):
    data = Patient.objects.filter(user__is_active=True)
    serializer = PatientSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#Esta vista trae la informacion de un solo paciente 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listPatient(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})

    serializer = PatientSerializer(patient, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK) 


#El paciente puede modificar su informacion
@api_view(['POST'])
@permission_classes([IsPatient])
def patientUpdate(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})

    serializer = PatientSerializer(instance=patient, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response('La informacion del paciente ha sido cambiada correctamente', status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsPatient])
def patientDelete(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()

    return Response('Patient successfully deleted')     
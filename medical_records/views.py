from rest_framework import status 
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from medical_records.models import MedicalRecord
from medical_records.serializers import MedicalRecordSerializer

from citas.permissions import IsPatient, IsOwner

from patients.models import Patient
from patients.serializers import BasicPatientSerializer 

#El paciente crea su historial medico
@api_view(['POST'])
@permission_classes([IsPatient, ])
def createMedicalRecord(request):
    '''
    {
        "patient": "id",
        "important_background": "Antecedentes importantes del paciente",
        "allergies": "Alergias",
        "reference": "Referencia",
        "family_background": "Antecedentes familiares",
        "pathological_background": "Antecedentes patologicos",
        "currently_medication": "Medicacion Actual",
        "surgeries": "Cirugias",
        "nonpath_background": "Antecedentes no patologicos",
        "smoking": "True/False",
        "drinking": "True/False",
        "gynecological_background": "Antecedentes ginecologicos",
        "system_interrogation": "Sistemas y aparatos del cuerpo"
    }
    '''
    data = request.data

    try:
        patient = Patient.objects.get(id=data['patient'])
    except:
        return Response({'Error': 'No hay un paciente con es id'})
    
    patient_serializer = BasicPatientSerializer(instance=patient, data=data, partial=True)
    patient_serializer.is_valid()

    serializer = MedicalRecordSerializer(data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

#El paciente consulta su Historial Medico
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listMedicalRecord(request, id_pat):
    try:
        patient = Patient.objects.filter(id=id_pat)
    except: 
        return Response({'Error': 'No hay un paciente con ese id'})
    medical_record = MedicalRecord.objects.filter(is_active=True, patient__in=patient)
    serializer = MedicalRecordSerializer(instance=medical_record, partial=True, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

#El paciente y el doctor que esta consultando al paciente pueden editar el historial medico
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateMedicalRecord(request, id_pat):
    data = request.data 
    try:
        patient = Patient.objects.filter(id=id_pat)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})

    medical_record = MedicalRecord.objects.filter(is_active=True, patient__in=patient).first()
    serializer = MedicalRecordSerializer(instance=medical_record, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response('Historial Medico editado correctamente', status=status.HTTP_200_OK)

#El paciente puede eliminar su propio historial medico
@api_view(['DELETE'])
@permission_classes([IsOwner])
def deleteMedicalRecord(request, id_pat):
    try:
        patient = Patient.objects.filter(id=id_pat)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    medical_record = MedicalRecord.objects.filter(patient__in=patient)
    medical_record.is_active = False
    medical_record.save()
    return Response('Su historial medico ha sido eliminado correctamente', status=status.HTTP_200_OK)

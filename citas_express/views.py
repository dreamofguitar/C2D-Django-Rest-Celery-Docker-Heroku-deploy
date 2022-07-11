from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from doctors.models import Doctor 

from patients.models import Patient 
from patients.serializers import BasicPatientSerializer

from citas_express.serializers import CitaExpressSerializer, BasicCitaExpSerializer
from citas_express.models import CitaExpress 
#PATIENT VIEWS

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCitaExp(request):
    '''
    {"patient": "<Patient.id>", "appointment_reason": "Razon de la cita"}
    ''' 
    try:
        patient = Patient.objects.get(id=request.data['patient'])
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    print(patient)
    patient_serializer = BasicPatientSerializer(instance=patient, data=request.data, partial=True)
    patient_serializer.is_valid()

    serializer = CitaExpressSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkCita(request, id):
    try:
        cita_exp = CitaExpress.objects.get(id=id)
    except:
        return Respnse({'Error': 'No hay una cita con ese id'})

    doc = cita_exp.doctor

    if doc == None:
        return Response('Su cita aun no ha sido aceptada')
    else:
        return Response('Su cita ha sido aceptada por el Doctor {}'.format(doc))


#DOCTORS VIEWS 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def waitingRoom(request):
    citas = CitaExpress.objects.filter(taken=False)
    serializer = BasicCitaExpSerializer(instance=citas, many=True, partial=True)

    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def takeCita(request, id):
    '''
    {
        "id_cita": "<str:id_cita>",
    }
    '''
    data = request.data
    try:
        doc = Doctor.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un doctor con ese id'})

    try:
        cita_exp = CitaExpress.objects.get(id=data['id_cita'])
    except:
        return Response({'Error': 'No hay una cita con ese id'})
    
    cita_exp.doctor = doc
    cita_exp.taken = True
    cita_exp.save()

    return Response("Cita aceptada en un momento iniciara la videollamada", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completeCitaExp(request, id):
    try:
        patient = Patient.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    
    cita_exp = CitaExpress.objects.get(patient=patient, completed=False)
    cita_exp.completed = True
    cita_exp.save()
    

    return Response('Su cita ha sido terminada correctamente', status=status.HTTP_200_OK)


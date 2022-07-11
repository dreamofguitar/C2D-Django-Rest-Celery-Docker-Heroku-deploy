import datetime
from datetime import timedelta
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from patients.serializers import BasicPatientSerializer 
from patients.models import Patient

from doctors.serializers import BasicDoctorSerializer 
from doctors.models import Doctor

from citas.serializers import (CitasSerializer, 
    DoctorCitasSerializer, 
    PatientCitasSerializer,
    BasicCitaSerializer)
from citas.permissions import IsOwner, IsPatient, IsDoctor 
from citas.models import Cita
from citas.tasks import citaReminder

#PATIENT VIEWS 

#El paciente crea una cita 
@api_view(['POST'])
@permission_classes([IsPatient, ])
def createCitas(request):
    '''
    Format input should be 
    {"date_time": "YYYY-MM-DD H:M", "patient": "<Patient.id>", "doctor": "<Doctor.id>", "appointment_type": "General", "appointment_reason": "Razon de la cita"}
    '''
    data = request.data 

    try:
        patient = Patient.objects.get(id=request.data['patient'])
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    patient_serializer = BasicPatientSerializer(instance=patient, data=data, partial=True)        
    patient_serializer.is_valid()

    try:
        doctor = Doctor.objects.get(id=request.data['doctor'])
    except:
        return Response({'Error': 'No hay un doctor con ese id'})
    doctor_serializer = BasicDoctorSerializer(instance=doctor, data=data, partial=True) 
    doctor_serializer.is_valid()   
    data['room'] = get_random_string(length=12, allowed_chars='ACTGXJLMU')
    cita_serializer = CitasSerializer(data=data, partial=True )
    cita_serializer.is_valid(raise_exception=True)
    cita_serializer.save()
    
    return Response(cita_serializer.data, status=status.HTTP_201_CREATED)


#El paciente consulta sus citas pendientes del dia que se hace la peticion en adelante
@api_view(['GET'])
@permission_classes([IsOwner, ])
def patListCita(request, id_pat):
    try:
        patient = Patient.objects.filter(id=id_pat)
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    citas = Cita.objects.filter(is_active=True, completed=False, patient__in=patient, date_time__gte=datetime.date.today())
    serializer = PatientCitasSerializer(citas, many=True, partial=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

#El paciente consulta sus citas canceladas, que ya pasaron, o las que fueron canceladas por el doctor 
@api_view(['POST'])
@permission_classes([IsOwner, ])
def citaCompletedList(request):
    '''
    {
        "id": "id_pat",
        "is_active": "True/False",
        "completed": "True/False",
        "accept": "True/False"
    }
    '''
    data = request.data 
    try:
        patient = Patient.objects.filter(id=data['id'])
    except:
        return Response({'Error': 'No hay un paciente con ese id'})
    citas = Cita.objects.filter(is_active=data['is_active'], completed=data['completed'], patient__in=patient)
    serializer = PatientCitasSerializer(citas, many=True, partial=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

#El paciente cancela una cita
@api_view(['PUT'])
@permission_classes([IsOwner, ])
def cancelCita(request, id):
    try:
        cita = Cita.objects.get(id=id)
    except:
        return Response({'Error': 'No hay una cita con ese id'})
    
    cita.is_active = False
    cita.save()
    return Response('Cita cancelada correctamente', status=status.HTTP_200_OK)


#                       DOCTOR VIEWS 

#El doctor acepta una cita
#En caso de ser aceptada se envia un correo al paciente 30 minutos antes de la cita 
@api_view(['POST'])
@permission_classes([IsDoctor, ])
def acceptCita(request, id):
    '''
    {"accept": "True/False"}
    '''
    data = request.data
    half_hour = timedelta(minutes=30)
    try:
        cita = Cita.objects.get(id=id)
    except:
        return Response({'Error': 'No hay una cita con ese id'})
    
    appointment_date = cita.date_time - half_hour
    
    serializer = BasicCitaSerializer(instance=cita, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

    if serializer.data['accept']:
        citaReminder.apply_async((id,), eta=appointment_date)
        return Response('Cita aceptada correctamente', status=status.HTTP_200_OK)
    else:
        return Response('Cita rechazada correctamente', status=status.HTTP_200_OK)


#El doctor consulta sus citas que tiene programadas y las que faltan por aceptar 
@api_view(['GET'])
@permission_classes([IsDoctor, ])
def docListCita(request, id_doc, mes, year):
    try:
        doctor = Doctor.objects.filter(id=id_doc)
    except:
        return Response({'Error': 'No hay un Doctor con ese id'})
    citas = Cita.objects.filter(is_active=True, doctor__in=doctor, date_time__month=mes, date_time__year=year)
    serializer = DoctorCitasSerializer(citas, many=True, partial=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


#El doctor da por completada una cita
@api_view(['POST'])
@permission_classes([IsDoctor, ])
def completeCita(request):
    '''
    {
        "id": "id",
        "completed": "True/False"
    }
    '''
    data = request.data
    try:
        cita = Cita.objects.get(id=data['id'])
    except:
        return Response({'Error': 'No hay una cita con ese id'})
    
    serializer = BasicCitaSerializer(instance=cita, data=data, parital=True)
    if serializer.is_valid():
        serializer.save()

    return Response('La cita ha sido completada correctamente', status=status.HTTP_200_OK)


#Para ver todas las citas con fines de pruebas!
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def listCitas(request):
    data = Cita.objects.all()
    serializer = CitasSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
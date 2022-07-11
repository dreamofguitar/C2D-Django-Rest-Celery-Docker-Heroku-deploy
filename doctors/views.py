from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from doctors.models import Doctor, Schedule
from doctors.serializers import DoctorSerializer, BasicDoctorSerializer,ScheduleSerializer

from users.serializers.users import UserSerializer

from citas.permissions import IsDoctor
#Doctor CRUD
@api_view(['POST'])
@permission_classes ([AllowAny])
def  CreateDoctors(request):
    '''
    Registers Doctor to the server. Input should be in the format:
    {"email": "email@test.com", "password": "1234abcd","name" : "Connect","first_name" : "To",
    "last_name" : "Doctors" ,"birthday" : "10/04/1998","phone": "444245612", 
    "gender":"0","client_type": "1", "curp":"MOSCAJ2352","fiscal_address":"5TH AVENUE 1235",
    "cfdi":"ASDQWF123","university" : "Oxfoard university", "professional_licence": "234142",
    "speciality": "Oncology","postgraduate":"High speciality", "address":"Maryland ST 1234","contact_phone":"2234452",
    "reference":"Near Princeston Plainsboro Hospital", "name_account_owner":"Leon F. Kennedy", "bank":"BBVA", "account":"23523544","clabe":"23422223"}
    '''
    
    data = request.data
    user_serializer = UserSerializer(data=data, partial=True)
    user_serializer.is_valid(raise_exception=True)
    user_serializer.save()
    data['user'] = user_serializer.instance.id
    serializer = DoctorSerializer(data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)    

@api_view(['POST'])
@permission_classes([IsDoctor])
def  UpdateDoctor(request, id):
    try:
        doctor = Doctor.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un Doctor con ese id'})
    serializer=DoctorSerializer(instance=doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes ([IsAuthenticated])
def  RetrieveDoctors(request):
    doctor = Doctor.objects.all()
    serializer=DoctorSerializer(doctor, many=True, partial=True)
    return Response(serializer.data,status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes ([IsAuthenticated])
def  RetrieveDoctor(request, id):
    try:
        doctor = Doctor.objects.get(id=id)
    except:
        return Response({'Error': 'No hay un Doctor con ese id'})
    serializer=DoctorSerializer(doctor, many=False, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes ([IsDoctor])
def  DeleteDoctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.is_active = False
    serializer=DoctorSerializer(instance=doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def SpecialDoctorList(request, speciality):
    data = Doctor.objects.filter(speciality=speciality)
    serializer = BasicDoctorSerializer(data, many=True, partial=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
#DOCTOR AVAILABILITY VIEWS
@api_view(['POST','PUT'])
@permission_classes([AllowAny])
def CreateSchedule(request):
    '''
        to create Schedule [{"doctor":"1", "day": 1, "month": 9, "hour": "08:00", "hour1": "09:00", "hour2": "10:00"},{"doctor":"1", "day": 2, "month": 9, "hour": "08:00", "hour1": "09:00", "hour2": "10:00"}]
    '''
    queryset = Schedule.objects.all()
    data = request.data
    serializer = ScheduleSerializer(queryset, data=data, many=True,partial=True)
    serializer.is_valid()
    serializer.save()
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def RetriveSchedule(request,id):

    try:
        doctor = Doctor.objects.filter(id=id)
    except:
        return Response({"Error":"No existe ese doctor"})

    schedule = Schedule.objects.filter(doctor__in=doctor)
    serializer = ScheduleSerializer(schedule,partial=True,many=True)
    

    return Response(serializer.data,status=status.HTTP_200_OK)

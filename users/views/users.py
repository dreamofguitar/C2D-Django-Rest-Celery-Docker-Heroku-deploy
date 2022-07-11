from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status

import requests 
from decouple import config
from users.serializers import UserSerializer, LoginUserSerializer
from users.models import User
from doctors.models import Doctor
from patients.models import Patient

# Create your views here.

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET') 

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"email": "email", "password": "1234abcd","name" : "Connect","first_name" : "To","last_name" : "Doctors" ,"birthday" : "10/04/1998","phone": "444245612", "gender":"Male/Female"}
    '''
    # Put the data from the request into the serializer 
    serializer = UserSerializer(data=request.data) 
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save() 
        # Then we get a token for the created user.
        # This could be done differentley 
        r = requests.post('http://127.0.0.1:8000/o/token/', 
            data={
                'grant_type': 'client_credentials',
                'email': request.data['email'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json())
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Gets tokens with email and password. Input should be in the format:
    {"email": "email", "password": "1234abcd"}
    '''
    r = requests.post(
    'https://conn2drs.herokuapp.com/o/token/', 
        data={
            'grant_type': 'password',
            'username': request.data['email'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    try:
        usuario = User.objects.get(email=request.data['email'])
    except: 
        return Response({"Error":"No hay una cuenta con ese email"})
    serializer = LoginUserSerializer(instance=usuario, many=False, partial=True)
    
    def getid(usuario):
        if usuario.client_type == 1:
            doc = Doctor.objects.get(user=usuario)
            return doc.id
        else: 
            pat = Patient.objects.get(user=usuario)
            return pat.id

    exact_id = getid(usuario)

    if r.status_code == 200:
        if serializer.data['is_active']:
            return Response((r.json(), 
                            {"client_type":serializer.data['client_type'],
                            "id":exact_id,
                            "email":serializer.data['email'],
                            "name":serializer.data['name'],
                            "first_name":serializer.data['first_name'],
                            "last_name":serializer.data['last_name']}))
        return Response({"Error":"Esta cuenta esta inactiva"})                    
    return Response(r.json()) 
    
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Registers user to the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    'https://conn2drs.herokuapp.com/o/token/', 
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json())

@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke tokens.
    {"token": "<token>"}
    '''
    r = requests.post(
        'https://conn2drs.herokuapp.com/o/revoke_token/', 
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response({'Message': 'Token revoked'}, r.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def emailverification(request):
    '''
    To verify email input like this json example
    {"email":"example@email.com"}
    '''
    try:
        user = User.objects.get(email=request.data['email'])
        return Response({"Este email ya esta registrado"})
    except:
        return Response({"Se puede usar este email"})    

from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from rest_framework.response import Response
from decouple import config
from citas.serializers import BasicCitaSerializer  
from citas.models import Cita
from django.utils.crypto import get_random_string
from .serializers import TWTestTokenSerializer
from .models import TWTestToken

@api_view(['POST'])
@permission_classes ([AllowAny])
def token(request):
    # User can ask for twilio token 
    '''
     Get Token with name and name room example {"name":"user","appointment_id":"id of appointment"}
    '''
    ACCOUNT_SID = config('ACCOUNT_SID')
    API_KEY_SID = config('API_KEY_SID')
    API_KEY_SECRET = config('API_KEY_SECRET')

    # Create an Access Token
    token = AccessToken(ACCOUNT_SID, API_KEY_SID, API_KEY_SECRET)

    try:
        cita = Cita.objects.get(id=request.data['appointment_id'])
    except:
        Response({"Error":"Cita no valida"})

    serializer = BasicCitaSerializer(cita, many=False, partial=True)
    # Set the Identity of this token
    token.identity = request.data['name']

    # Grant access to Video
    grant = VideoGrant(room=serializer.data['room'])
    token.add_grant(grant)
    return Response ((token.to_jwt(),{"room":serializer.data['room']}))


@api_view(['POST'])
@permission_classes ([AllowAny])
def save_twtest_token(request):

    '''
    Save the token and room {"token":"token","room":"room example"}
    '''
    data = request.data
    serializer = TWTestTokenSerializer(data=data, many=False)
    serializer.is_valid()
    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permission_classes ([AllowAny])
def retrieve_twtest_token(request):
 
    try:
        test_token = TWTestToken.objects.filter(status=True).first()
        test_token.status = False
        serializer = TWTestTokenSerializer(instance=test_token,data=request.data,many =False,partial=True)
        serializer.is_valid()
        serializer.save()


        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"Error":"No hay tokens validos"})

@api_view(['GET'])
@permission_classes ([AllowAny])
def retrieve_all_twtest_token(request):
    token = TWTestToken.objects.all()
    serializer=TWTestTokenSerializer(token, many=True, partial=True)
    return Response(serializer.data,status = status.HTTP_200_OK)

#@api_view(['POST'])
#@permission_classes ([AllowAny])
#def retrieve_twtest_token(request):
# 
#    
#    test_token = TWTestToken.objects.filter(status=True).first()
#    serializer = TWTestTokenSerializer(instance=test_token,data=request.data,many =False,partial=True)
#  serializer.is_valid()
#    serializer.save()
#
#
#   return Response(serializer.data, status=status.HTTP_200_OK)
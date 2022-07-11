from django.shortcuts import render
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .checkCedula import getCedula
from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([AllowAny])

def CheckCedula(request):
    if request.method=='GET':
        response_a = getCedula(request.GET["cedula"])
        return JsonResponse(response_a)
    else:
        return Response(content, status=status.HTTP_404_NOT_FOUND)  
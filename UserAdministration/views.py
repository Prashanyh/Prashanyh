from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,views
from rest_framework.decorators import api_view, permission_classes, authentication_classes
# import requests
import random
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
# from .utils import Util,otp_generator
import jwt

from django.contrib import messages
from django.shortcuts import get_object_or_404
from .serializers import *



class RegisterApi(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request, *args,  **kwargs):
        parameters = request.data.copy()
        # parameters['otp'] = random.randrange(1000, 10000)
        serializer = self.get_serializer(data=parameters)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"message": "User Created Successfully.  Now perform Login to get your token"},status=status.HTTP_201_CREATED)
        else:
            return Response({'Mobile number already exist'},status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status,views
from rest_framework import generics
from .serializers import *
from rest_framework.views import APIView



class RegisterApi(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request, *args,  **kwargs):
        parameters = request.data.copy()
        serializer = self.get_serializer(data=parameters)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"message": "User Created Successfully.  Now perform Login to get your token"},status=status.HTTP_201_CREATED)
        else:
            return Response({'user name already exist'},status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class WorkingUrls(APIView):
    # test url
    def get(self, request, format=None):
        word = 'urls working fine'
        return Response({'response': word},status=status.HTTP_200_OK)


from rest_framework import serializers
from .models import *
import re
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    # mobile = serializers.RegexField("[0-9]{10}",min_length=10,max_length=10)
    password = serializers.CharField(write_only=True)
    email=serializers.EmailField(max_length=155,min_length=3,required=True)
    name=serializers.CharField(max_length=55,min_length=3,required=True)

    class Meta:
        model = UserProfile
        fields = ("id","name", "email", "password", "mobile","dob","gender")
        # fields="__all__"



    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)

    class Meta:
        model= UserProfile
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    mobile=serializers.CharField()
    password=serializers.CharField(max_length=10,min_length=6,write_only=True)
    name=serializers.CharField(max_length=255,min_length=3,read_only=True)
    tokens=serializers.CharField(max_length=135,min_length=6,read_only=True)

    class Meta:
        model= UserProfile
        fields=['mobile','password','name','tokens']


    def validate(self, attrs):
        mobile = attrs.get('mobile', '')
        password = attrs.get('password', '')
        user = auth.authenticate(mobile=mobile,password=password)
        # import pdb
        # pdb.set_trace()
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled , contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('user is not verified')

        return {
            'mobile':user.mobile,
            'name':user.name,
            'tokens':user.tokens
        }


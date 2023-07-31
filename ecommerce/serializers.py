from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], email=attrs['email'],
        password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        return user

class CartSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Cart
        fields = '__all__'

    
class BuySerializer(serializers.ModelSerializer):

    class Meta:
        model = Buy
        fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

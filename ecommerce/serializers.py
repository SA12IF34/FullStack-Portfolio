from rest_framework import serializers
from .models import *

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class BoughtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bought
        fields = '__all__'

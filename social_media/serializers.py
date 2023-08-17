from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__' 
    
class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    file = serializers.FileField(required=False)

    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowNotification
        fields = '__all__'
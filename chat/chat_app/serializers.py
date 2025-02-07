from rest_framework import serializers
from django.contrib.auth.models import User
from .models import GroupChat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupChat  # Update Group to GroupChat
        fields = '__all__'
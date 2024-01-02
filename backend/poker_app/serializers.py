from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        ref_name = 'CustomUser'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'players']
        read_only_fields = ['id', 'players']

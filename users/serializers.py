from rest_framework import serializers

from .models import PokerUser


class PokerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokerUser
        fields = ['id', 'username']

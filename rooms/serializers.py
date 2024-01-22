from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'n_players', 'starting_chips', 'big_blind_value']
        read_only_fields = ['id', 'players']


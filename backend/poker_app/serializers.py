from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Game, Player, Card, CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        ref_name = 'CustomUser'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'players']
        read_only_fields = ['id', 'players']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['suit', 'rank']


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'chips', 'highest_combination', 'pot', 'is_folded', 'is_all_in',
                  'round_bet', 'can_check', 'can_raise', 'can_call']

from django.db import models
from poker_app.models import CustomUser

class Game(models.Model):
    room_name = models.CharField(max_length=255)
    is_started = models.BooleanField(default=False)
    round_status = models.CharField(max_length=255)
    summary_pot = models.IntegerField(default=0)
    starting_chips = models.IntegerField(default=1000)
    big_blind_value = models.IntegerField(default=0)
    small_blind_value = models.IntegerField(default=0)
    current_player_move = models.IntegerField(default=0)
    dealer_index = models.IntegerField(default=0)
    small_blind_player = models.IntegerField(default=0)
    big_blind_player = models.IntegerField(default=0)
    total_players_count = models.IntegerField(default=0)
    round_number = models.IntegerField(default=0)

class Players(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    balance_in_game = models.IntegerField(default=1000)
    personal_pot_in_round = models.IntegerField(default=0)
    highest_combination = models.CharField(max_length=255)
    is_playing_status = models.BooleanField(default=0)
    index_in_table = models.IntegerField(default=0)
    all_in_status = models.BooleanField(default=False)
    can_check_status = models.BooleanField(default=False)
    can_raise_status = models.BooleanField(default=False)
    is_small_blind = models.BooleanField(default=False)
    is_big_blind = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)
    round_number = models.IntegerField(default=0)

class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    suit = models.CharField(max_length=255)
    rank = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
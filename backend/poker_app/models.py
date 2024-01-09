from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    chips = models.IntegerField(default=1000)

    def __str__(self):
        return self.username


class Room(models.Model):
    name = models.CharField(max_length=255)
    max_players = models.PositiveIntegerField(default=2)
    players = models.ManyToManyField(CustomUser, blank=True, related_name='rooms')
    is_game_started = models.BooleanField(default=False)


class Game(models.Model):
    max_players = models.IntegerField(default=8)
    players_connected = models.IntegerField(default=0)
    dealer = models.IntegerField(default=0)
    current_player = models.IntegerField(default=0)
    big_blind_player = models.IntegerField(default=0)
    small_blind_player = models.IntegerField(default=0)
    starting_chips = models.IntegerField(default=1000)
    small_blind = models.IntegerField(default=25)
    big_blind = models.IntegerField(default=50)
    last_raise = models.IntegerField(default=0)
    biggest_bet = models.IntegerField(default=0)
    rounds_played = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    all_played = models.BooleanField(default=False)
    game_over = models.BooleanField(default=False)
    round_ended = models.BooleanField(default=False)
    game_initialized = models.BooleanField(default=False)
    game_in_progress = models.BooleanField(default=False)
    path = models.CharField(max_length=30)
    name = models.SlugField(max_length=30)


class Player(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    last_action = models.CharField(max_length=20, blank=True)
    last_raise = models.IntegerField(default=0)
    in_game_order = models.IntegerField(default=0)
    chips = models.IntegerField(default=0)
    highest_combination = models.IntegerField(default=0)
    pot = models.IntegerField(default=0)
    round_bet = models.IntegerField(default=0)
    is_in_game = models.BooleanField(default=False)
    can_check = models.BooleanField(default=False)
    can_raise = models.BooleanField(default=False)
    can_call = models.BooleanField(default=False)
    is_folded = models.BooleanField(default=False)
    is_all_in = models.BooleanField(default=False)


class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True)
    suit = models.CharField(max_length=10)
    rank = models.CharField(max_length=2)
    value = models.IntegerField()
    order = models.IntegerField(default=0)
    location = models.CharField(default='DECK', max_length=6)

    def __str__(self):
        return '{} - {}'.format(self.suit, self.rank)

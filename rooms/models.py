from django.db import models

from users.models import PokerUser


class Room(models.Model):
    name = models.CharField(max_length=255)
    is_game_started = models.BooleanField(default=False)

    max_players = models.PositiveIntegerField(default=7)
    n_players = models.IntegerField(default=0)

    starting_chips = models.IntegerField(default=1000)
    big_blind_value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} | id: {self.id}'

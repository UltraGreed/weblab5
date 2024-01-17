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

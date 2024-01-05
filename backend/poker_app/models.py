from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    max_players = models.PositiveIntegerField(default=4)
    players = models.ManyToManyField(User, blank=True, related_name='rooms')
    invitations = models.ManyToManyField(User, blank=True, related_name='room_invitations')

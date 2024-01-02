from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    players = models.ManyToManyField(User, blank=True)

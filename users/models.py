from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class PokerUser(AbstractUser):
    chips = models.IntegerField(default=1000)

    def __str__(self):
        return self.username

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import PokerUser

admin.site.register(PokerUser, UserAdmin)

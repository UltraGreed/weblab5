from django.urls import path
from .views import GetMe


urlpatterns = [
    # path('', get_user_list, name='user-list'),
    path('me/', GetMe.as_view(), name='get-me')
]

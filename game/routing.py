from django.urls import re_path

from .poker_consumer import PokerConsumer

websocket_urlpatterns = [
    re_path(r"ws/room/(?P<room_id>\d+)/$", PokerConsumer.as_asgi()),
]
from django.urls import re_path
import gameplay.consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<game_name>\w+)/$', gameplay.consumers.GameConsumer.as_asgi()),
]

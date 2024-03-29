import os

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

from game.routing import websocket_urlpatterns

from game.poker_game_manager import PokerGameManager

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokerscuf.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
    "channel": ChannelNameRouter({
        "poker-game-manager": PokerGameManager.as_asgi(),
    }),
})

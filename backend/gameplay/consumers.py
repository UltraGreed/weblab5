from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .db_calls import *
from poker_app.serializers import UserSerializer, GameSerializer


def get_parameter_value(parameters, key):
    found = [par for par in parameters if key in par]
    found = found[0] if len(found) > 0 else None
    return found[found.find('=') + 1:] if found is not None else None


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.query_string = self.scope['query_string'].decode('utf-8').split('&')

        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        user = await get_user(get_parameter_value(self.query_string, 'user'))
        game = await get_game(get_parameter_value(self.query_string, 'game'))

        players_all = await get_players(game)

        self.player_id = await create_player(user, game, players_all)

        players_in_game = await get_players(game, True)

        self.connect_data = {}

        if await init_game(game, players_in_game):
            if not game.game_in_progress:
                game = await get_game_by_id(game.id)
                await start_first_round(game, players_in_game)

            self.connect_data['start_game'] = True

        else:
            self.connect_data['start_game'] = False

        self.connect_data['user'] = UserSerializer(user).data['id']
        self.connect_data['game'] = GameSerializer(game).data['id']
        self.connect_data['type'] = 'player_connected'

        await self.channel_layer.group_send(self.game_group_name, self.connect_data)

    async def disconnect(self, code):
        await disconnect_player(self.player_id, self.game_name)
        self.data = {
            "type": 'player_disconnected'
        }
        await self.channel_layer.group_send(self.game_group_name, self.data)
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(self.game_group_name, content)

    async def player_connected(self, message):
        await self.send_json(content=message)

    async def player_disconnected(self, message):
        await self.send_json(content=message)

    async def player_action(self, message):
        game = await get_game_by_name(self.game_name)
        await game_helper.next_player(game)
        message['current_player'] = await get_current_player(self.game_name)
        await self.send_json(content=message)

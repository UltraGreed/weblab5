from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .db_calls import *
from poker_app.serializers import UserSerializer, GameSerializer


def get_parameter_value(parameters, key):
    found = [par for par in parameters if key in par]
    found = found[0] if len(found) > 0 else None
    return found[found.find('=') + 1:] if found is not None else None


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_name']
        self.game_group_name = 'game_%s' % self.game_name
        self.query_string = self.scope['query_string'].decode('utf-8').split('&')

        await self.channel_layer.group_add(
            self.game_group_name, self.channel_name
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

        await self.accept()

    async def disconnect(self, code):
        await disconnect_player(self.player_id, self.game_name)
        self.data = {
            "type": 'player_disconnected'
        }
        await self.channel_layer.group_send(self.game_group_name, self.data)
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        action_type = content.get('type', None)

        if action_type == 'raise':
            await self.handle_raise(content)
        elif action_type == 'call':
            await self.handle_call(content)
        elif action_type == 'all_in':
            await self.handle_all_in(content)
        elif action_type == 'bet':
            await self.handle_bet(content)
        elif action_type == 'check':
            await self.handle_check(content)
        elif action_type == 'fold':
            await self.handle_fold(content)

    async def handle_raise(self, content):
        game_name = content['game']
        player_id = self.player_id
        chips = int(content['value'])

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.raize(player, chips)
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'raise', 'chips': chips}
        await self.channel_layer.group_send(self.game_group_name, message)

    async def handle_call(self, content):
        game_name = content['game']
        player_id = self.player_id
        chips = int(content['value'])

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.call(player, chips)
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'call', 'chips': chips}
        await self.channel_layer.group_send(self.game_group_name, message)

    async def handle_all_in(self, content):
        game_name = content['game']
        player_id = self.player_id
        chips = int(content['value'])

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.all_in(player, chips)
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'all_in', 'chips': chips}
        await self.channel_layer.group_send(self.game_group_name, message)

    async def handle_bet(self, content):
        game_name = content['game']
        player_id = self.player_id
        chips = int(content['value'])

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.bet(player, chips)
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'bet', 'chips': chips}
        await self.channel_layer.group_send(self.game_group_name, message)

    async def handle_check(self, content):
        game_name = content['game']
        player_id = self.player_id

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.check()
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'check'}
        await self.channel_layer.group_send(self.game_group_name, message)

    async def handle_fold(self, content):
        game_name = content['game']
        player_id = self.player_id

        player = await get_player_by_id(player_id)
        game = await get_game_by_name(game_name)

        player_helper.fold(player)
        await game_helper.check_next_round(game_name)

        message = {'type': 'player_action', 'action': 'fold'}
        await self.channel_layer.group_send(self.game_group_name, message)
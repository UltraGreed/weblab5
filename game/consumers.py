import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from .poker_game import PokerGame


# noinspection PyArgumentList
class PokerConsumer(WebsocketConsumer):
    games = []

    def __init__(self):
        super().__init__()
        self.room_id = 0
        self.room_group_name = ''
        self.game = None
        self.user = None

    def connect(self):
        self.user = self.scope['user']
        if not self.user.is_authenticated:
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        if self.room_group_name not in PokerConsumer.games:
            PokerConsumer.games[self.room_id] = PokerGame(
                lambda data: async_to_sync(self.channel_layer.group_send)(self.room_group_name, data)
            )

        self.game = PokerConsumer.games[self.room_id]

        if not self.game.check_player(self.user['id']):
            self.game.add_player(self.user['id'], self.user['username'])

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "player.joined",
                    "player_id": self.user.id,
                    "username": self.user['username']
                }
            )

        if self.game.countdown:
            self.send_countdown(self.game.countdown)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        self.game.remove_player(self.user['id'])

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "player.left",
                "player_id": self.user.id
            }
        )

        # TODO: room removal

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        # TODO: receive turn answers

    def send_countdown(self, event):
        self.send(text_data=json.dumps({
            'type': 'countdown',
            'countdown': event['countdown'],
        }))

    def player_joined(self, event):
        self.send(text_data=json.dumps({
            'type': 'player_joined',
            'player_id': event['player_id'],
            'username': event['username']
        }))

    def player_left(self, event):
        self.send(text_data=json.dumps({
            'type': 'player_left',
            'player_id': event['player_id'],
        }))

    def game_started(self, event):
        self.send(text_data=json.dumps({
            'type': 'game_started',
            'dealer_id': event['dealer_id']
        }))

    def cards_dealt(self, event):
        self.send(text_data=json.dumps({
            'type': 'cards_dealt',
            'player_cards': event['players'][self.user.id]['cards']
        }))

    def awaiting_turn(self, event):
        self.send(text_data=json.dumps({
            'type': 'awaiting_turn',
            'player_id': event['player_id'],
            'was_raised': event['was_raised']
        }))

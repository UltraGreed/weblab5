import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from .poker_game import PokerGame

from rooms.models import Room
from users.models import PokerUser


# noinspection PyArgumentList
class PokerConsumer(WebsocketConsumer):
    games = {}

    def __init__(self):
        super().__init__()
        self.room_id = 0
        self.room_group_name = ''
        self.game = None
        self.user = None

    def connect(self):
        self.user = self.scope['user']

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        if not self.user.is_authenticated:
            return 'Not authenticated'

        if self.room_id in PokerConsumer.games:
            game = PokerConsumer.games[self.room_id]
            if game.check_full():
                return 'Room full'
            elif game.check_started():
                return 'Room started'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        if self.room_group_name not in PokerConsumer.games:
            PokerConsumer.games[self.room_id] = PokerGame(
                self.room_id,
                lambda data: async_to_sync(self.channel_layer.group_send)(self.room_group_name, data)
            )

        self.game = PokerConsumer.games[self.room_id]

        if not self.game.check_player(self.user.id):
            self.game.add_player(self.user.id, self.user.username)

            room = Room.objects.get(id=self.room_id)
            room.n_players += 1
            room.save()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "player.joined",
                    "player_id": self.user.id,
                    "username": self.user.username
                }
            )

        if self.game.countdown:
            self.send_countdown(self.game.countdown)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        self.game.remove_player(self.user.id)

        room = Room.objects.get(id=self.room_id)
        room.n_players -= 1
        room.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "player.left",
                "player_id": self.user.id
            }
        )

        # TODO: room removal

    def receive(self, text_data):
        event_json = json.loads(text_data)
        event_type = event_json['type']

        if event_type == 'player_action':
            player_id = event_json['player_id']
            action = event_json['action']
            player_chips = PokerUser.objects.get(id=player_id).chips
            amount = event_json['amount']
            self.game.player_action(player_id, player_chips, action, amount)

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
            'player_cards': ['_'.join(card) for card in event['players'][self.user.id]['cards']]
        }))

    def common_cards_dealt(self, event):
        self.send(text_data=json.dumps({
            'type': 'common_cards_dealt',
            'cards': ['_'.join(card) for card in event['cards']]
        }))

    def awaiting_turn(self, event):
        self.send(text_data=json.dumps({
            'type': 'awaiting_turn',
            'player_id': event['player_id'],
            'was_raised': event['was_raised'],
            'current_bet': event['current_bet'],
            'bank': event['bank']
        }))

    def action_confirmed(self, event):
        self.send(text_data=json.dumps({
            'type': 'action_confirmed',
            'player_id': event['player_id'],
            'action': event['action'],
            'amount': event['amount']
        }))

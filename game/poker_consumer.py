import json

from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from rooms.models import Room


# noinspection PyArgumentList
class PokerConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.room_id = 0
        self.room_group_name = ''
        self.user = None
        self.qualified = False

    def connect(self):
        self.user = self.scope['user']

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        if not self.user.is_authenticated:
            self.disconnect('Not authenticated')

        self.accept()
        # noinspection PyUnresolvedReferences
        async_to_sync(self.channel_layer.send)(
            'poker-game-manager',
            {
                'type': 'player.connected',
                'user_id': self.user.id,
                'chips_requested': Room.objects.get(id=self.room_id).starting_chips,
                'room_id': self.room_id,
                'channel': self.channel_name
            }
        )

    def player_connected_verdict(self, event):
        if not event['is_qualified']:
            self.disconnect(event['reason'])

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.send)(
            'poker-game-manager',
            {
                'type': 'get.players.data',
                'room_id': self.room_id,
                'channel': self.channel_name
            }
        )

    def send_players_data(self, event):
        self.send(text_data=json.dumps({
            'type': 'players_data',
            'players': [
                {'player_id': p_id, 'username': p['username'], 'chips': p['chips']}
                for p_id, p in event['players'].items()
            ]
        }))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.send)(
            'poker-game-manager',
            {
                'type': 'player.disconnected',
                'player_id': self.user.id,
                'room_id': self.room_id
            }
        )

    # noinspection PyMethodOverriding
    def receive(self, text_data):
        event_json = json.loads(text_data)
        event_type = event_json['type']

        if event_type == 'player_action':
            async_to_sync(self.channel_layer.send)(
                'poker-game-manager',
                {
                    'type': 'player.action',
                    'user_id': self.user.id,
                    'action': event_json['action'],
                    'chips_action': event_json['chips_action'],
                    'room_id': self.room_id
                }
            )

    def send_countdown(self, event):
        self.send(text_data=json.dumps({
            'type': 'countdown',
            'countdown': event['countdown'],
        }))

    def player_joined(self, event):
        self.send(text_data=json.dumps({
            'type': 'player_joined',
            'player_id': event['player_id'],
            'username': event['username'],
            'chips': event['chips']
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
            'player_cards': ['_'.join(card) for card in event['players'][str(self.user.id)]['cards']]
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
            'chips_action': event['chips_action'],
            'chips_remaining': event['chips_remaining']
        }))

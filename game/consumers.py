import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .poker_game import PokerGame


class PokerConsumer(WebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.room_id = 0
        self.room_group_name = ''

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"room_{self.room_id}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()


        if not self.room_group_name in PokerConsumer.games:
            PokerConsumer.games[self.room_group_name] = PokerGame([])

        PokerConsumer.games[self.room_group_name].players.append({
            'username': 'hui',
            'cards': [],
        })

        if len(PokerConsumer.games[self.room_group_name].players) > 1:
            PokerConsumer.games[self.room_group_name].shuffle_deck()
            PokerConsumer.games[self.room_group_name].give_cards()
            PokerConsumer.games[self.room_group_name].deal_community_cards()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "update_game"}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "update_game"}
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        if message == "next_round" and (len(PokerConsumer.games[self.room_group_name].players) > 1):
            PokerConsumer.games[self.room_group_name].next_round()

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "update_game"}
            )

    def update_game(self, event):
        self.send(text_data=json.dumps({
            'message': 'update_game',
            'game_state': PokerConsumer.games[self.room_group_name].to_dict(),
        }))

PokerConsumer.games = {}

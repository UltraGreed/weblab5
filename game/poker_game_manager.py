from asgiref.sync import async_to_sync, sync_to_async
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async

from game.poker_game import PokerGame
from rooms.models import Room


# noinspection PyArgumentList
class PokerGameManager(SyncConsumer):
    games = {}

    @staticmethod
    def create_game(event):
        room_id = event['room_id']
        room_group_name = f"room_{room_id}"
        PokerGameManager.games[room_id] = PokerGame(
            room_id,
            room_group_name
        )

    @staticmethod
    def player_connected(event):
        PokerGameManager.games[event['room_id']].player_connected(event)

    @staticmethod
    def get_players_data(event):
        PokerGameManager.games[event['room_id']].get_players_data(event)

    @staticmethod
    def player_disconnected(event):
        PokerGameManager.games[event['room_id']].player_disconnected(event)

    @staticmethod
    def player_action(event):
        PokerGameManager.games[event['room_id']].player_action(event)
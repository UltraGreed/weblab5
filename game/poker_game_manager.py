from channels.consumer import AsyncConsumer

from game.poker_game import PokerGame


# noinspection PyArgumentList
class PokerGameManager(AsyncConsumer):
    games = {}

    @staticmethod
    async def create_game(event):
        room_id = event['room_id']
        room_group_name = f"room_{room_id}"
        PokerGameManager.games[room_id] = await PokerGame.create(
            room_id,
            room_group_name
        )

    @staticmethod
    async def player_connected(event):
        await PokerGameManager.games[event['room_id']].player_connected(event)

    @staticmethod
    async def get_players_data(event):
        await PokerGameManager.games[event['room_id']].get_players_data(event)

    @staticmethod
    async def player_disconnected(event):
        await PokerGameManager.games[event['room_id']].player_disconnected(event)

    @staticmethod
    async def player_action(event):
        await PokerGameManager.games[event['room_id']].player_action(event)
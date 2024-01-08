from channels.db import database_sync_to_async
from poker_app import player_helper, card_helper, game_helper
from poker_app.models import Game, Player
from poker_app.serializers import GameSerializer
from poker_app.models import CustomUser


@database_sync_to_async
def get_user(user_id):
    if user_id is None:
        return 'user not logged in'
    return CustomUser.objects.filter(id=user_id).first()


@database_sync_to_async
def get_game(game_path):
    if game_path is None:
        return 'no slug received'
    game_path = game_path[0:-1] if game_path[-1] == '/' else game_path
    return Game.objects.filter(path=game_path).first()


@database_sync_to_async
def get_game_by_name(name):
    if name is None:
        return 'no name received'
    return Game.objects.filter(name=name).first()


@database_sync_to_async
def get_game_by_id(game_id):
    return Game.objects.filter(id=game_id).first()


@database_sync_to_async
def create_player(user, game, players):
    players = players.order_by('in_game_order')
    player = players.filter(user=user).first()
    if player is None:
        player = Player(user=user, name=user.username, game=game, chips=GameSerializer(game).data['starting_chips'],
                        is_in_game=True)
    else:
        player.is_in_game = True

    if len(players) < 1:
        player.in_game_order = 1
    else:
        player.in_game_order = players.reverse()[0].in_game_order + 1

    game.players_connected = len(players)
    game.save()

    player.save()
    return player.id


@database_sync_to_async
def disconnect_player(player_id, game_name):
    game = Game.objects.filter(name=game_name).first()
    players = Player.objects.filter(game=game)
    player = players.filter(id=player_id).first()
    if player is not None:
        player_helper.adjust_orders(player, players)
        player.is_in_game = False
        game.players_connected -= 1
        game.save()

        player.save()
    else:
        print('warn, player not found')


@database_sync_to_async
def init_game(game, players):
    if len(players) > 1:
        if not game.game_initialized:
            game_helper.init_game(game, players)
            card_helper.init_cards(game)

            card_helper.deal_cards(game, players)
        return True
    return False


@database_sync_to_async
def start_first_round(game, players):
    player_helper.set_blinds(game, players)
    game.game_in_progress = True
    game.save()


@database_sync_to_async
def get_players(game, in_game_only=False):
    if in_game_only:
        return Player.objects.filter(game=game, is_in_game=True)
    return Player.objects.filter(game=game)


@database_sync_to_async
def get_current_player(game_name):
    game = Game.objects.filter(name=game_name).first()
    if game is not None:
        return game.current_player
    return 0

from django.db.models import F
from poker_app.models import Game


def adjust_orders(removed_player, players):
    players.filter(in_game_order__gte=removed_player.in_game_order).update(in_game_order=F('in_game_order') - 1)
    removed_player.in_game_order = 0
    removed_player.save()


def set_blinds(game, players):
    bb_player = players.filter(id=game.big_blind_player).first()
    sb_player = players.filter(id=game.small_blind_player).first()
    bb_player = bet(bb_player, game.big_blind)
    sb_player = bet(sb_player, game.small_blind)

    bb_player.save()
    sb_player.save()


def bet(player, value):
    if value < player.chips:
        player.chips -= value
        player.round_bet += value
        return player
    player.round_bet = player.chips
    player.chips = 0
    player.is_all_in = True
    return player


def raize(player, value):
    player = bet(player, value)
    game = Game.objects.filter(id=player.game.id).first()
    # game = game_helper.new_bet(game, value, player.round_bet)
    player.save()
    game.save()


def call(game, player):
    call_val = player.round_bet - game.biggest_bet
    player = bet(player, call_val)
    # game = game_helper.new_bet(game, call_val, player.pot)
    player.save()
    game.save()


def all_in(game, player):
    player.round_bet += player.chips
    # game = game_helper.new_bet(game, player.chips, player.pot)
    player.chips = 0
    player.is_all_in = True
    player.save()
    game.save()


def check():
    return


def fold(player):
    player.is_in_game = False
    player.save()


def set_allowed_actions(game, player):
    player.can_check = can_check(game, player)
    player.can_call = can_call(game, player)
    player.can_raise = can_raise(game, player)
    player.can_fold = player.is_in_game
    player.can_all_in = player.is_in_game
    return player


def can_check(game, player):
    if game.biggest_bet <= player.round_bet:
        return True
    return False


def can_call(game, player):
    if (game.biggest_bet - player.pot) <= player.chips:
        return True
    return False


def can_raise(game, player):
    if (game.biggest_bet + game.last_raise - player.pot) <= player.chips:
        return True
    return False


def reset_round_bets(players):
    for player in players:
        player.pot += player.round_bet
        player.round_bet = 0
        player.save()

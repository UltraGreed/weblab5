import random
from .models import Card
from gameplay_utils.deck import Deck
from . import utils


def _create_deck(game):
    deck = Deck()
    for card in deck.set:
        Card.objects.create(game=game, suit=card.suit, rank=card.rank,
                            value=card.value)


def _delete_deck(game):
    Card.objects.filter(game=game).delete()


def _shuffle(game):
    cards = Card.objects.filter(game=game, location='DECK')
    order_numbers = list(range(len(cards)))
    random.shuffle(order_numbers)
    for i, n in enumerate(order_numbers):
        cards[i].order = n
        cards[i].save()


def _get_cards(game, limit):
    return Card.objects.filter(game=game, location='DECK').order_by('order')[:limit]


def _deal_cards_for_player(player, cards):
    for card in cards:
        card.player = player
        card.location = 'HAND'
        card.save()


def deal_cards(game, players):
    cards = utils.chunks(_get_cards(game, (len(players) * 2)), 2)
    for player in players:
        _deal_cards_for_player(player, next(cards))


def init_cards(game):
    _delete_deck(game)
    _create_deck(game)
    _shuffle(game)


def deal_cards_table(game, n):
    cards = _get_cards(game, n)
    for card in cards:
        card.location = 'TABLE'
        card.save()


def get_player_cards(player):
    return Card.objects.filter(player=player)


def get_table_cards(game):
    return Card.objects.filter(game=game, location='TABLE')

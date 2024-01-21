import random
import time

from asgiref.sync import async_to_sync


def generate_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    return [(suit, rank) for rank in ranks for suit in suits]


default_deck = generate_deck()


# noinspection PyArgumentList
class PokerGame:
    timer = 30

    def __init__(self, send_message_func):
        self._players = {}

        self._deck = default_deck.copy()
        random.shuffle(self._deck)

        self._common_cards = []

        self._countdown = 0

        self._send_message = send_message_func

    def deal_cards(self):
        for _ in range(2):
            for player in self._players.values():
                card = self._deck.pop()
                player['cards'].append(card)

    def drop_cards(self):
        for player in self._players.values():
            player['cards'] = []

    def deal_common_cards(self):
        if self._common_cards == 0:
            for _ in range(3):
                card = self._deck.pop()
                self._common_cards.append(card)
        elif self._common_cards == 3 or self._common_cards == 4:
            card = self._deck.pop()
            self._common_cards.append(card)

    def reset_game(self):
        self._deck = default_deck.copy()
        random.shuffle(self._deck)

        self._common_cards = []

        self.drop_cards()

    def start_countdown(self):
        self._countdown = PokerGame.timer

        self._send_message({
            'type': 'send.countdown',
            'countdown': self.countdown,
        })

        while self.countdown:
            time.sleep(1)
            self._countdown -= 1

        self.start_game()

    def start_game(self):
        dealer_id = random.choice(self._players.keys())

        self._send_message({
            'type': 'game.started',
            'dealer_id': dealer_id
        })

        self.deal_cards()

        self._send_message({
            'type': 'cards.dealt',
            'players': self._players
        })

        self._send_message({
            'type': 'awaiting.turn',
            'player_id': dealer_id,
            'was_raised': False
        })

        # self.deal_common_cards()
        #
        # for _ in range(3):
        #     card = self._deck.pop()
        #     self._common_cards.append(card)
        #
        # self.reset_game()

    @property
    def countdown(self):
        return self._countdown

    def add_player(self, player_id, username):
        self._players[player_id] = {'username': username, 'cards': [], 'folded': False}

        if len(self._players) >= 2:
            self.start_countdown()

    def remove_player(self, player_id):
        self._players.pop(player_id)

    def check_player(self, player_id):
        return player_id in self._players

    def player_action(self, player_id, action):
        pass
        # TODO: implement player action

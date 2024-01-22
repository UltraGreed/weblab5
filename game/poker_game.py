import random
import time
from rooms.models import Room


def generate_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    return [(suit, rank) for rank in ranks for suit in suits]


default_deck = generate_deck()


# noinspection PyArgumentList
class PokerGame:
    timer = 10

    def __init__(self, room_id, send_message_func):
        self._players = {}
        self._turn_player_id = 0

        self._was_raised = False
        self._raised_player_id = 0

        self._is_game_started = False

        self._room_id = room_id
        room = Room.objects.get(id=room_id)
        self._max_players = room.max_players
        self._starting_chips = room.starting_chips
        self._min_bet = room.big_blind_value

        self._bank = 0
        self._current_bet = 0

        self._first_player_id = 0

        self._deck = default_deck.copy()
        random.shuffle(self._deck)

        self._common_cards = []

        self._countdown = 0

        self._send_message = send_message_func

        self._game_turn = []

    def _deal_cards(self, amount):
        for _ in range(amount):
            for player in self._players.values():
                card = self._deck.pop()
                player['cards'].append(card)

    def _drop_cards(self):
        for player in self._players.values():
            player['cards'] = []

    def _deal_common_cards(self, amount):
        for _ in range(amount):
            card = self._deck.pop()
            self._common_cards.append(card)

    def _reset_game(self):
        self._deck = default_deck.copy()
        random.shuffle(self._deck)

        self._common_cards = []

        self._drop_cards()
        # TODO: implement actual reset

    def _start_countdown(self):
        self._countdown = PokerGame.timer

        self._send_message({
            'type': 'send.countdown',
            'countdown': self.countdown,
        })

        while self.countdown:
            time.sleep(1)
            self._countdown -= 1

        self._game_turn = self._game_turn_gen()
        next(self._game_turn)

    def _game_turn_gen(self):
        dealer_id = random.choice(self._players.keys())
        self._first_player_id = dealer_id
        self._raised_player_id = dealer_id

        self._send_message({
            'type': 'game.started',
            'dealer_id': dealer_id
        })

        self._deal_cards(2)

        self._send_message({
            'type': 'cards.dealt',
            'players': self._players
        })

        self._turn_player_id = dealer_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(3)

        self._send_message({
            'type': 'common.cards.dealt',
            'players': self._players
        })

        self._first_player_id = self._get_next_player(self._first_player_id)
        self._turn_player_id = self._first_player_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(1)

        self._send_message({
            'type': 'common.cards.dealt',
            'cards': self._common_cards
        })

        self._first_player_id = self._get_next_player(self._first_player_id)
        self._turn_player_id = self._first_player_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(1)

        self._send_message({
            'type': 'common.cards.dealt',
            'players': self._players
        })

        self._first_player_id = self._get_next_player(self._first_player_id)
        self._turn_player_id = self._first_player_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._game_end()

    def _game_end(self):
        winner_id = self._get_winner()

        self._send_message({
            "type": 'game.end',
            'winner_id': winner_id,
            'bank': self._bank
        })

        # TODO: implement wa-bank and high card split
        # TODO: restart game

    @property
    def countdown(self):
        return self._countdown

    def add_player(self, player_id, username):
        self._players[player_id] = {'username': username, 'cards': [], 'folded': False, 'bet': 0}

        if len(self._players) >= 2:
            self._start_countdown()

    def remove_player(self, player_id):
        self._players.pop(player_id)

    def check_player(self, player_id):
        return player_id in self._players

    def check_full(self):
        return len(self._players) >= self._max_players

    def check_started(self):
        return self._is_game_started

    def player_action(self, player_id, player_chips, action, raise_amount=0):
        if player_id != self._turn_player_id:
            return "Not your turn"
        if not self._is_game_started:
            return "Game not started yet"

        player = self._players[player_id]

        if (self._was_raised and action == 'call' or
                not self._was_raised and action == 'check'):
            bet = self._current_bet - player['bet']

            if bet > player_chips:
                return "Not enough chips"

            self._bank += bet
            player['bet'] = self._current_bet

            # TODO: Substract chips

        elif (self._was_raised and action == 'raise' or
              not self._was_raised and action == 'bet'):
            if self._current_bet + raise_amount > self._starting_chips:
                return "Bet too high"
            if self._min_bet > raise_amount:
                return "Bet too low"

            self._bank += raise_amount
            self._current_bet += raise_amount
            self._raised_player_id = self._turn_player_id
            player['bet'] = self._current_bet

            # TODO: Substract chips

        elif action == 'fold':
            player['folded'] = True

        else:
            return 'Incorrect action'

        self._send_action_confirmed(action, raise_amount)
        self._send_next_turn()
        self._turn_player_id = self._get_next_player(self._turn_player_id)

        if self._turn_player_id == self._raised_player_id:
            if len(list(filter(lambda p: not p['folded'], self._players))) == 1:
                self._game_end()
                return

            next(self._game_turn)

        # TODO: implement player action

    def _send_action_confirmed(self, action, amount):
        self._send_message({
            'type': 'action.confirmed',
            'player_id': self._turn_player_id,
            'action': action,
            'amount': amount
        })

    def _send_next_turn(self):
        self._send_message({
            'type': 'awaiting.turn',
            'player_id': self._turn_player_id,
            'was_raised': self._was_raised,
            'current_bet': self._current_bet,
            'bank': self._bank
        })

    def _get_next_player(self, player_id):
        next_player_id = (player_id + 1) % len(self._players)
        while self._players[next_player_id]['folded']:
            next_player_id = (next_player_id + 1) % len(self._players)
        return next_player_id

    def _get_winner(self):
        return 0
        # TODO: determine winner from combinations



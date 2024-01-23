import random
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rooms.models import Room
from users.models import PokerUser


def generate_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    return [(suit, rank) for rank in ranks for suit in suits]


default_deck = generate_deck()


# noinspection PyArgumentList
class PokerGame:
    timer = 10

    def __init__(self, room_id, room_group_name):
        self._players = {}
        self._turn_player_id = 0

        self.channel_layer = get_channel_layer()

        self._was_raised = False
        self._raised_player_id = 0

        self._is_game_started = False

        self._room_id = room_id
        self._room_group_name = room_group_name

        # noinspection PyUnresolvedReferences
        self._room = Room.objects.get(id=room_id)
        self._max_players = self._room.max_players
        self._starting_chips = self._room.starting_chips
        self._min_bet = self._room.big_blind_value

        self._bank = 0
        self._current_bet = 0

        self._first_player_id = 0

        self._deck = default_deck.copy()
        random.shuffle(self._deck)

        self._common_cards = []

        self._countdown = 0

        self._game_turn = iter([])

    def player_connected(self, event):
        user_id = event['user_id']
        user = PokerUser.objects.get(pk=user_id)
        print(event)
        consumer_channel = event['channel']
        verdict = {}
        if user_id in self._players.keys():
            verdict['is_qualified'] = True
            verdict['reason'] = 'ok'
        elif len(self._players) >= self._max_players:
            verdict['is_qualified'] = False
            verdict['reason'] = 'room-full'
        elif self._is_game_started:
            verdict['is_qualified'] = False
            verdict['reason'] = 'game-already-started'
        elif event['chips_requested'] < self._starting_chips or event['chips_requested'] > user.chips:
            verdict['is_qualified'] = False
            verdict['reason'] = 'not-enough-chips'
        else:
            verdict['is_qualified'] = True
            verdict['reason'] = 'ok'

        async_to_sync(self.channel_layer.send)(
            consumer_channel,
            {
                'type': 'player.connected.verdict',
                **verdict
            }
        )

        if verdict['is_qualified'] and user_id not in self._players.keys():
            self._players[str(user.id)] = {
                'username': user.username,
                'chips': event['chips_requested'],
                'cards': [],
                'folded': False,
                'bet': 0
            }

            async_to_sync(self.channel_layer.group_send)(
                self._room_group_name,
                {
                    "type": "player.joined",
                    "player_id": user.id,
                    "username": user.username,
                    'chips': event['chips_requested']
                }
            )

            self._room.n_players += 1
            self._room.save()

            if len(self._players) >= 2 and not self._countdown and not self._is_game_started:
                self._start_countdown()

    def player_disconnected(self, event):
        # noinspection PyUnresolvedReferences
        room = Room.objects.get(id=self._room_id)
        room.n_players -= 1
        room.save()

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                "type": "player.left",
                "player_id": event['player_id']
            }
        )
        # TODO: room removal

    def get_players_data(self, event):
        async_to_sync(self.channel_layer.send)(
            event['channel'],
            {
                'type': 'send.players.data',
                'players': self._players
            }
        )

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

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'send.countdown',
                'countdown': self._countdown,
            })

        while self._countdown:
            time.sleep(1)
            self._countdown -= 1

        self._room.is_game_started = True
        self._room.save()

        self._is_game_started = True
        self._game_turn = self._game_turn_gen()
        next(self._game_turn)

    def _game_turn_gen(self):
        dealer_id = random.choice(list(self._players.keys()))
        self._first_player_id = dealer_id
        self._raised_player_id = dealer_id

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'game.started',
                'dealer_id': dealer_id
            })

        self._deal_cards(2)

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'cards.dealt',
                'players': self._players
            })

        self._turn_player_id = dealer_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(3)

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'common.cards.dealt',
                'players': self._players
            })

        self._first_player_id = self._get_next_player(self._first_player_id)
        self._turn_player_id = self._first_player_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(1)

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'common.cards.dealt',
                'cards': self._common_cards
            })

        self._first_player_id = self._get_next_player(self._first_player_id)
        self._turn_player_id = self._first_player_id
        self._was_raised = False

        self._send_next_turn()

        yield

        self._deal_common_cards(1)

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
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

        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                "type": 'game.end',
                'winner_id': winner_id,
                'bank': self._bank
            }
        )

        # TODO: implement wa-bank and high card split
        # TODO: restart game

    def player_action(self, event):
        user = PokerUser.objects.get(pk=event['user_id'])
        action = event['action']
        chips_action = event['chips_action']

        if user.id != self._turn_player_id:
            return "Not your turn"
        if not self._is_game_started:
            return "Game not started yet"

        player = self._players['user.id']

        if (self._was_raised and action == 'call' or
                not self._was_raised and action == 'check'):
            bet = self._current_bet - player['bet']

            if bet > user.chips:
                return "Not enough chips"

            self._bank += bet
            player['bet'] = self._current_bet

            # TODO: Substract chips

        elif (self._was_raised and action == 'raise' or
              not self._was_raised and action == 'bet'):
            if self._current_bet + chips_action > self._starting_chips:
                return "Bet too high"
            if self._min_bet > chips_action:
                return "Bet too low"

            self._bank += chips_action
            self._current_bet += chips_action
            self._raised_player_id = self._turn_player_id
            player['bet'] = self._current_bet

            # TODO: Substract chips

        elif action == 'fold':
            player['folded'] = True

        else:
            return 'Incorrect action'

        self._send_action_confirmed(action, chips_action)
        self._send_next_turn()
        self._turn_player_id = self._get_next_player(self._turn_player_id)

        if self._turn_player_id == self._raised_player_id:
            if len(list(filter(lambda p: not p['folded'], self._players))) == 1:
                self._game_end()
                return

            next(self._game_turn)

        # TODO: implement player action

    def _send_action_confirmed(self, action, chips_action, chips_remaining):
        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'action.confirmed',
                'player_id': self._turn_player_id,
                'action': action,
                'chips_action': chips_action,
                'chips_remaining': chips_remaining
            }
        )

    def _send_next_turn(self):
        async_to_sync(self.channel_layer.group_send)(
            self._room_group_name,
            {
                'type': 'awaiting.turn',
                'player_id': self._turn_player_id,
                'was_raised': self._was_raised,
                'current_bet': self._current_bet,
                'bank': self._bank
            }
        )

    def _get_next_player(self, player_id):
        next_player_id = (player_id + 1) % len(self._players)
        while self._players[next_player_id]['folded']:
            next_player_id = (next_player_id + 1) % len(self._players)
        return next_player_id

    def _get_winner(self):
        return 0
        # TODO: determine winner from combinations


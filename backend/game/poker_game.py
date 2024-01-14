import random

class PokerGame:
    def __init__(self, players):
        self.players = players
        self.deck = self.generate_deck()
        self.shuffle_deck()
        self.community_cards = []
        self.current_player = 0

    def generate_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        return [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def give_cards(self):
        for _ in range(2):
            for player in self.players:
                card = self.deck.pop()
                player['cards'].append(card)

    def clean_cards(self):
        for player in self.players:
            player['cards'] = []

    def deal_community_cards(self):
        for _ in range(3):
            card = self.deck.pop()
            self.community_cards.append(card)

    def next_round(self):
        if len(self.community_cards) < 5:
            card = self.deck.pop()
            self.community_cards.append(card)
        else:
            self.deck = self.generate_deck()
            self.community_cards = []
            self.shuffle_deck()
            self.give_cards()
            self.clean_cards()
            self.give_cards()
            self.deal_community_cards()

    def to_dict(self):
        return {
            'players': self.players,
            'community_cards': self.community_cards,
            'current_player': self.current_player,
        }

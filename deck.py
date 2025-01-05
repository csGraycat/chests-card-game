import random


def create_standard_deck():
    default_deck = []
    suits = ["\u2663", "\u2665",
             "\u2666", "\u2660"]
    ranks = ["A", "K", "Q", "J"] + list(range(6, 11))
    for suit in suits:
        for rank in ranks:
            default_deck.append(str(rank) + suit)
    return default_deck


class Deck:
    def __init__(self):
        self.cards = create_standard_deck()

    def shuffle(self):
        shuffled = []
        cards = self.cards
        for _ in range(len(cards)):
            card = random.choice(cards)
            shuffled.append(card)
            cards.remove(card)
        self.cards = shuffled

    def pick_card(self):
        return random.choice(self.cards)

    def deal_random_cards(self, amount):
        dealt = []
        for _ in range(amount):
            card = self.pick_card()
            dealt.append(card)
            self.cards.remove(card)
        return dealt

    def deal_from_top(self, amount):
        dealt = self.cards[:amount]
        self.cards = self.cards[amount:]
        return dealt

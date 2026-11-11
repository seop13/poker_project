"""카드 한 장(Card)과 카드 52장 묶음(Deck)을 다루는 모듈"""
import random

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# '2' -> 2, ..., 'J' -> 11, 'Q' -> 12, 'K' -> 13, 'A' -> 14
RANK_VALUES = {rank: value for value, rank in enumerate(RANKS, start=2)}


class Card:
    """카드 한 장"""

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_up = False  # 앞면이 보이는 상태인지

    @property
    def value(self):
        """족보 계산용 숫자 값"""
        return RANK_VALUES[self.rank]

    @property
    def is_red(self):
        return self.suit in ('♥', '♦')

    def flip(self):
        """카드를 뒤집는다"""
        self.face_up = not self.face_up

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class Deck:
    """카드 52장 묶음"""

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        """맨 위에서 카드 한 장을 뽑는다"""
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

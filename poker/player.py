"""플레이어(나, 컴퓨터)를 다루는 모듈"""


class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.is_computer = is_computer
        self.hand = []  # 손에 든 카드 2장

    def receive(self, card):
        """카드 한 장을 받는다"""
        self.hand.append(card)

    def clear_hand(self):
        """다음 게임을 위해 손패를 비운다"""
        self.hand = []

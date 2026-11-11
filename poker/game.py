"""게임 진행 규칙을 담당하는 모듈 (화면과는 분리)"""
from .deck import Deck
from .player import Player
from .evaluator import best_hand, hand_name


class Game:
    def __init__(self):
        self.player = Player('나')
        self.computer = Player('컴퓨터', is_computer=True)
        self.deck = None
        self.board = []      # 바닥에 깔린 공용 카드
        self.is_over = False

    def start_round(self):
        """새 게임: 덱을 섞고 2장씩 나눠준 뒤 바닥에 3장(플랍)을 깐다"""
        self.deck = Deck()
        self.board = []
        self.is_over = False
        self.player.clear_hand()
        self.computer.clear_hand()

        for _ in range(2):
            self.player.receive(self.deck.draw())
            self.computer.receive(self.deck.draw())

        for _ in range(3):
            self._deal_to_board()

    def _deal_to_board(self):
        card = self.deck.draw()
        card.face_up = True
        self.board.append(card)

    def is_board_full(self):
        return len(self.board) == 5

    def check(self):
        """체크: 바닥에 한 장 더 깐다.
        이미 5장이 깔려 있으면 쇼다운을 하고 결과를 돌려준다."""
        if not self.is_board_full():
            self._deal_to_board()
            return None
        return self.showdown()

    def fold(self):
        """폴드: 이번 게임은 패배"""
        self.is_over = True
        return {'winner': 'computer', 'folded': True}

    def showdown(self):
        """모든 카드를 공개하고 승자를 가린다"""
        self.is_over = True
        for card in self.player.hand + self.computer.hand:
            card.face_up = True

        player_score = best_hand(self.player.hand + self.board)
        computer_score = best_hand(self.computer.hand + self.board)

        if player_score > computer_score:
            winner = 'player'
        elif player_score < computer_score:
            winner = 'computer'
        else:
            winner = 'tie'

        return {
            'winner': winner,
            'folded': False,
            'player_hand': hand_name(player_score),
            'computer_hand': hand_name(computer_score),
        }

"""Tkinter 화면 모듈: 시작 화면과 게임 테이블을 그린다"""
import tkinter as tk

from .game import Game
from .card_view import CardView, EmptySlot

TABLE_COLOR = '#0b6623'
TEXT_COLOR = 'white'
FONT = 'Arial'


class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Poker')
        self.root.geometry('760x660')
        self.root.configure(bg=TABLE_COLOR)
        self.root.resizable(False, False)

        self.game = Game()
        self.result = None  # 게임이 끝나면 결과가 들어간다

        self.show_start_screen()

    # ---------- 공통 ----------
    def clear(self):
        """화면의 모든 위젯을 지운다"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def label(self, text, size=14, bold=False, **pack_options):
        weight = 'bold' if bold else 'normal'
        widget = tk.Label(self.root, text=text, fg=TEXT_COLOR, bg=TABLE_COLOR,
                          font=(FONT, size, weight))
        widget.pack(**pack_options)
        return widget

    # ---------- 시작 화면 ----------
    def show_start_screen(self):
        self.clear()
        self.label('POKER', size=60, bold=True, pady=(180, 10))
        self.label('컴퓨터와 1:1 텍사스 홀덤', size=14)
        tk.Button(self.root, text='게임 시작', font=(FONT, 16, 'bold'),
                  width=12, command=self.start_game).pack(pady=40)

    # ---------- 게임 화면 ----------
    def start_game(self):
        self.game.start_round()
        self.result = None
        self.render_table()

    def render_table(self):
        """현재 게임 상태대로 테이블을 다시 그린다"""
        self.clear()
        game = self.game

        self.draw_cards('컴퓨터', game.computer.hand, clickable=False)
        self.draw_cards('바닥', game.board, clickable=False, slots=5)
        self.draw_cards('나  (카드를 클릭하면 뒤집혀요)', game.player.hand,
                        clickable=not game.is_over)

        controls = tk.Frame(self.root, bg=TABLE_COLOR)
        controls.pack(pady=20)

        if self.result is None:
            check_text = '체크 (결과 보기)' if game.is_board_full() else '체크'
            tk.Button(controls, text=check_text, font=(FONT, 14), width=14,
                      command=self.on_check).pack(side='left', padx=10)
            tk.Button(controls, text='폴드', font=(FONT, 14), width=10,
                      command=self.on_fold).pack(side='left', padx=10)
        else:
            self.draw_result(controls)

    def draw_cards(self, title, cards, clickable, slots=None):
        """제목과 카드 한 줄을 그린다. slots가 있으면 빈 자리도 그린다."""
        self.label(title, size=13, bold=True, pady=(16, 6))
        row = tk.Frame(self.root, bg=TABLE_COLOR)
        row.pack()
        for card in cards:
            CardView(row, card, clickable).pack(side='left', padx=6)
        if slots:
            for _ in range(slots - len(cards)):
                EmptySlot(row).pack(side='left', padx=6)

    def draw_result(self, parent):
        result = self.result
        if result['folded']:
            message = '폴드했어요. 이번 게임은 패배!'
            detail = ''
        else:
            message = {'player': '이겼어요!',
                       'computer': '졌어요...',
                       'tie': '비겼어요!'}[result['winner']]
            detail = f"나: {result['player_hand']}   /   컴퓨터: {result['computer_hand']}"

        tk.Label(parent, text=message, fg='#ffd54f', bg=TABLE_COLOR,
                 font=(FONT, 18, 'bold')).pack()
        if detail:
            tk.Label(parent, text=detail, fg=TEXT_COLOR, bg=TABLE_COLOR,
                     font=(FONT, 13)).pack(pady=4)
        tk.Button(parent, text='게임 시작', font=(FONT, 14, 'bold'), width=12,
                  command=self.start_game).pack(pady=8)

    # ---------- 버튼 동작 ----------
    def on_check(self):
        self.result = self.game.check()
        self.render_table()

    def on_fold(self):
        self.result = self.game.fold()
        self.render_table()

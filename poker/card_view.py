"""카드 한 장을 화면에 그리는 모듈"""
import tkinter as tk

CARD_W = 80
CARD_H = 116

RED = '#c0392b'
BLACK = '#222222'
BACK_COLOR = '#1e3a8a'
BACK_LINE = '#93c5fd'


class CardView(tk.Canvas):
    """카드 그림. clickable=True면 클릭할 때마다 앞/뒤가 뒤집힌다."""

    def __init__(self, master, card, clickable=False):
        super().__init__(master, width=CARD_W, height=CARD_H,
                         bg=master['bg'], highlightthickness=0)
        self.card = card
        if clickable:
            self.config(cursor='hand2')
            self.bind('<Button-1>', self.on_click)
        self.draw()

    def on_click(self, event):
        self.card.flip()
        self.draw()

    def draw(self):
        self.delete('all')
        if self.card.face_up:
            self._draw_front()
        else:
            self._draw_back()

    def _draw_front(self):
        color = RED if self.card.is_red else BLACK
        self.create_rectangle(2, 2, CARD_W - 2, CARD_H - 2,
                              fill='white', outline='#999999', width=1)
        # 왼쪽 위: 숫자 + 무늬
        self.create_text(9, 6, text=self.card.rank, anchor='nw',
                         fill=color, font=('Arial', 14, 'bold'))
        self.create_text(9, 26, text=self.card.suit, anchor='nw',
                         fill=color, font=('Arial', 12))
        # 가운데: 큰 무늬
        self.create_text(CARD_W / 2, CARD_H / 2 + 4, text=self.card.suit,
                         fill=color, font=('Arial', 34))
        # 오른쪽 아래: 숫자
        self.create_text(CARD_W - 9, CARD_H - 6, text=self.card.rank, anchor='se',
                         fill=color, font=('Arial', 14, 'bold'))

    def _draw_back(self):
        self.create_rectangle(2, 2, CARD_W - 2, CARD_H - 2,
                              fill=BACK_COLOR, outline='white', width=2)
        self.create_rectangle(9, 9, CARD_W - 9, CARD_H - 9,
                              outline=BACK_LINE, width=1)
        # 격자무늬
        for x in range(17, CARD_W - 9, 10):
            self.create_line(x, 9, x, CARD_H - 9, fill='#2c4fae')
        for y in range(17, CARD_H - 9, 10):
            self.create_line(9, y, CARD_W - 9, y, fill='#2c4fae')
        self.create_text(CARD_W / 2, CARD_H / 2, text='♠',
                         fill=BACK_LINE, font=('Arial', 22))


class EmptySlot(tk.Canvas):
    """아직 카드가 깔리지 않은 바닥 자리"""

    def __init__(self, master):
        super().__init__(master, width=CARD_W, height=CARD_H,
                         bg=master['bg'], highlightthickness=0)
        self.create_rectangle(3, 3, CARD_W - 3, CARD_H - 3,
                              outline='#4caf50', dash=(4, 3))

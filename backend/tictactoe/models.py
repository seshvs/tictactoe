import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .board import PLAYER1, PLAYER2

PLAYER_1_STR = 'Player 1'
PLAYER_2_STR = 'Player 2'


# Create your models here.
class TicTacToe(models.Model):

    PLAYER_1_WIN = 'Player 1 Win'
    PLAYER_2_WIN = 'Player 2 Win'
    DRAW = 'DRAW'
    PROGRESS = 'PROGRESS'

    RESULT_CHOICE = (
        (PLAYER_1_WIN, PLAYER_1_WIN),
        (PLAYER_2_WIN, PLAYER_2_WIN),
        (DRAW, DRAW),
        (PROGRESS, PROGRESS)
    )
    PLAYER_CHOICE = {
        (PLAYER_1_STR, PLAYER_1_STR),
        (PLAYER_2_STR, PLAYER_2_STR)
    }
    board = models.TextField(_('board details'), max_length=100, null=False, blank=False)
    result = models.CharField(_('result field'), max_length=100, choices=RESULT_CHOICE, default=PROGRESS)
    player_start = models.CharField(_('player starting game'), max_length=100, choices=PLAYER_CHOICE,
                                    default=PLAYER_1_STR)
    player_1_choice = models.CharField(_('player one choice'), max_length=10, default=PLAYER1)
    player_2_choice = models.CharField(_('player two choice'), max_length=10, default=PLAYER2)

    is_computer_game = models.BooleanField(_('is player2 a computer'), default=False)
    created_at = models.DateTimeField(_('started at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def get_board(self):
        return json.JSONDecoder().decode(self.board)

    def set_board(self, board):
        self.board = json.dumps(board)

    def set_winning_state(self, game_over, who_won):
        if game_over:
            self.result = self.DRAW
            if who_won in [PLAYER1, PLAYER2]:
                self.result = self.PLAYER_1_WIN if who_won == PLAYER1 else self.PLAYER_2_WIN

    def set_result(self, choice):
        if (choice, choice) not in self.RESULT_CHOICE:
            raise Exception("Invalid choice")

        self.result = choice

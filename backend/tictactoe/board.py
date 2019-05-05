from math import inf
from random import choice

from rest_framework.exceptions import ValidationError

PLAYER1 = -1
PLAYER2 = 1
DRAW = 0


class BoardAlgorithm:

    def __init__(self, board=None):
        self.board = board

        self.player_1 = PLAYER1
        self.player_2 = PLAYER2

        if not board:
            self.board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

    def evaluate(self):
        if self.is_winning(self.player_2):
            return PLAYER2

        if self.is_winning(self.player_1):
            return PLAYER1

        return DRAW

    def is_winning(self, player):

        board = self.board

        wining_states = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]

        return True if [player, player, player] in wining_states else False

    def is_game_over(self):
        return self.is_winning(self.player_1) or self.is_winning(self.player_2)

    def get_empty_cells(self):
        cells = []
        for x, row in enumerate(self.board):
            for y, col in enumerate(row):
                if not col:
                    cells.append([x, y])

        return cells

    def set_move(self, x, y, player):

        if [x, y] in self.get_empty_cells():
            self.board[x][y] = player
            return True

        return False

    def minimax_optimised(self, depth, player):
        """
        Computer is always player 2
        """
        board = self.board
        best_case = [-1, -1, -inf] if player == self.player_2 else [-1, -1, +inf]

        if depth == 0 or self.is_game_over():
            score = self.evaluate()
            return [-1, -1, score]

        for x, y in self.get_empty_cells():
            board[x][y] = player
            score = BoardAlgorithm(board).minimax_optimised(depth - 1, -player)
            board[x][y] = 0
            score[0], score[1] = x, y

            if player == self.player_2 and score[2] > best_case[2]:
                best_case = score
            elif player == self.player_1 and score[2] < best_case[2]:
                best_case = score

        return best_case

    def human_turn(self, move, curr_player):
        from .models import PLAYER_1_STR

        depth = len(self.get_empty_cells())
        game_over = self.is_game_over()
        if depth == 0 or game_over:
            return self.board, game_over, self.evaluate()

        # Dictionary of valid moves
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }
        coord = moves[move]
        player = self.player_1 if curr_player == PLAYER_1_STR else self.player_2
        can_move = self.set_move(coord[0], coord[1], player)

        if any([move < 1, move > 9, not can_move]):
            raise ValidationError("Invalid move")

        return self.board,  self.is_game_over(), self.evaluate()

    def computer_turn(self):

        depth = len(self.get_empty_cells())
        game_over = self.is_game_over()
        if depth == 0 or game_over:
            return self.board, game_over, self.evaluate()

        if depth == 9:
            # First move. Get some random values
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            move = self.minimax_optimised(depth, self.player_2)
            x, y = move[0], move[1]

        self.set_move(x, y, self.player_2)

        return self.board, self.is_game_over(), self.evaluate()

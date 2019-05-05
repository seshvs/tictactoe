import json

from rest_framework import generics, status
from django.core import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .board import BoardAlgorithm
from .models import PLAYER_1_STR, PLAYER_2_STR, TicTacToe
from .serializers import TictactoeSerializer


class Tictactoe(generics.UpdateAPIView,
                generics.ListCreateAPIView):
    permission_classes = []
    serializer_class = TictactoeSerializer
    queryset = TicTacToe.objects.all()
    lookup_field = 'id'

    def _handle_computer_turn(self, board, game_id):
        board_obj = BoardAlgorithm(board)
        _, game_over, who_won = board_obj.computer_turn()

        # Let's update the board
        tictactoe = get_object_or_404(TicTacToe, id=game_id)
        tictactoe.set_board(board_obj.board)
        tictactoe.set_winning_state(game_over, who_won)
        tictactoe.save()

        serializer = json.loads(serializers.serialize('json', [tictactoe, ]))[0]

        response = serializer['fields']
        response['next_turn'] = PLAYER_1_STR
        response['id'] = serializer['pk']

        return response

    def update(self, request, *args, **kwargs):
        """ Use this to  ---- """
        if any([request.data["player"] not in [PLAYER_1_STR, PLAYER_2_STR],
                request.data["move"] > 9,
                request.data["move"] < 1,
                'id' not in request.data]):
            raise ValidationError("Incorrect data")

        game = get_object_or_404(TicTacToe, id=request.data["id"])
        board = game.get_board()
        board_obj = BoardAlgorithm(board)
        _, game_over, who_won = board_obj.human_turn(move=request.data["move"], curr_player=request.data["player"])

        # Lets update the human turn
        game.set_board(board_obj.board)
        game.set_winning_state(game_over, who_won)
        game.save()

        response_data = json.loads(serializers.serialize('json', [game, ]))[0]['fields']
        response_data['id'] = request.data['id']
        response_data['next_turn'] = PLAYER_2_STR if request.data['player'] == PLAYER_1_STR else PLAYER_1_STR

        if game.is_computer_game:
            response_data = self._handle_computer_turn(board_obj.board, response_data['id'])

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Use HTTP POST Method to start a game.
        """
        required_keys = ['player_start', 'is_computer_game']
        for key in required_keys:
            if key not in request.data:
                raise ValidationError('player_start (or) is_computer_game not available')

        data = request.data

        if 'board' not in request.data:
            data['board'] = json.dumps(BoardAlgorithm().board)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = serializer.data

        response_data['next_turn'] = PLAYER_1_STR if data['player_start'] == PLAYER_1_STR else PLAYER_2_STR

        if request.data['is_computer_game'] and data['player_start'] == PLAYER_2_STR:
            # Update the computer turn in the board
            response_data = self._handle_computer_turn(json.JSONDecoder().decode(data['board']), response_data['id'])

        return Response(response_data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))

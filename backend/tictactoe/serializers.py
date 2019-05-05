from rest_framework import serializers
from .models import TicTacToe


class TictactoeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicTacToe
        fields = '__all__'

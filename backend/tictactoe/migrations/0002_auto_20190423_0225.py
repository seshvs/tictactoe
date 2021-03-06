# Generated by Django 2.1.7 on 2019-04-23 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tictactoe',
            name='is_computer_game',
            field=models.BooleanField(default=False, verbose_name='is player2 a computer'),
        ),
        migrations.AddField(
            model_name='tictactoe',
            name='player_start',
            field=models.CharField(choices=[('Player 2', 'Player 2'), ('Player 1', 'Player 1')], default='Player 1', max_length=100, verbose_name='player starting game'),
        ),
    ]

from django.urls import path  # add this

from .views import Tictactoe

urlpatterns = [
    path('', Tictactoe.as_view(), name='game')
]

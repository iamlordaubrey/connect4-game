from django.urls import path

from game.views import JoinRoomView, EndGameView

urlpatterns = [
    path('join/', JoinRoomView.as_view(), name='join_room'),
    path('end/', EndGameView.as_view(), name='end_game'),
]

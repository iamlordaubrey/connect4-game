from django.shortcuts import render
from rest_framework import generics

from game.models import Game, GameHistory
from game.serializers import GameRoomSerializer, EndGameSerializer


class JoinRoomView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameRoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'player-id': self.request.headers.get('player-id')})
        return context


class EndGameView(generics.CreateAPIView):
    queryset = GameHistory.objects.all()
    serializer_class = EndGameSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #
    #     print('incoming request: ', request.data)
    #     if serializer.is_valid():
    #         pass
    #     else:
    #         print(serializer.errors)
    #     return super().post(self, request, *args, **kwargs)

from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from game.models import Game
from game.serializers import GameRoomSerializer
from player.models import Player


class JoinRoomView(generics.CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameRoomSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'player-id': self.request.headers.get('player-id')})
        return context
#
#
#     def get_serializer(self, *args, **kwargs):
#         serializer_class = self.get_serializer_class()
#         kwargs.setdefault('context', self.get_serializer_context())
#
#         """
#         Intercepting the request to access player-id in request.headers
#         """
#         player_id = self.request.headers.get('player-id')
#
#
# class JoinView(APIView):
#     def get(self, request):
#         player_id = request.headers.get('player-id')
#         player = Player.objects.get(id=player_id)
#         if not player:
#             raise APIException('Player not found')
#
#         game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()
#         if not game:
#             game = Game.objects.create()
#         game.players.add(player)
#
#         return Response({
#             'status': 'success',
#             'data': {'game': GameSerializer(instance=game).data}
#         })

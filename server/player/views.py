from rest_framework.response import Response
from rest_framework.views import APIView

from player.models import Player
from player.serializers import PlayerSerializer

class CreateView(APIView):
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        player_obj, created = Player.objects.get_or_create(username=username)

        return Response({
            'status': 'success',
            'data': {'player': PlayerSerializer(instance=player_obj).data, 'created': created}
        })

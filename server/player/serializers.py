from rest_framework import serializers

from player.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        model = Player
        fields = '__all__'

    def create(self, validated_data):
        player_obj, _ = Player.objects.get_or_create(username=validated_data['username'])
        return player_obj
        # def post(self, request):
        #     serializer = PlayerSerializer(data=request.data)
        #     serializer.is_valid(raise_exception=True)
        #
        #     username = serializer.validated_data['username']
        #     player_obj, created = Player.objects.get_or_create(username=username)
        #
        #     return Response({
        #         'status': 'success',
        #         'data': {'player': PlayerSerializer(instance=player_obj).data, 'created': created}
        #     })

# class PlayerSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True)
#
#     class Meta:
#         model = Player
#         fields = '__all__'


# {
#     "status": "success",
#     "data": {
#         "player": {
#             "id": "2e58d961-812d-4a58-932c-b83b5a923da0",
#             "username": "aubrey",
#             "created_at": "2023-08-31T11:13:33.917953Z",
#             "updated_at": "2023-08-31T11:13:33.918053Z",
#             "wins": 0,
#             "losses": 0
#         },
#         "created": true
#     }
# }
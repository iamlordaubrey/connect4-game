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

from django.db.models import Count
from rest_framework import serializers

from game.models import Game, GameHistory
from player.models import Player
from player.serializers import PlayerSerializer


class GameRoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Game
        fields = '__all__'

    @staticmethod
    def _get_players_count(obj):
        return obj.players.count()

    def create(self, validated_data):
        player_id = self.context['player-id']
        player = Player.objects.get(id=player_id)
        if not player:
            raise serializers.ValidationError('Player not found')

        # ToDo: Use player_one and player_two; Remove many-to-many relationship
        game = Game.objects.annotate(players_count=Count('players')).filter(players_count=1, started=False).first()

        if game:
            if player is not game.player_one:
                game.player_two = player
                game.save()
        else:
            game = Game.objects.create(player_one=player)

        game.players.add(player)
        if self._get_players_count(game) == 2:
            game.started = True
            game.save()

        return game


class EndGameSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(required=True)
    player_one_id = serializers.CharField(max_length=200, required=False)
    player_two_id = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = GameHistory
        fields = '__all__'

    def create(self, validated_data):
        game_id = validated_data['game_id']
        game = Game.objects.get(id=game_id)
        player_one = game.player_one
        player_two = game.player_two

        custom_validated_data = {
            **validated_data,
            'player_one_id': player_one.id,
            'player_two_id': player_two.id
        }

        return super().create(custom_validated_data)

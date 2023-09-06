from collections import defaultdict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from game.models import Game
from player.models import Player


class GameConsumer(AsyncJsonWebsocketConsumer):
    room_connection_count = defaultdict(lambda: 0)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name = None

    # ToDo: Move getters to utils file
    @database_sync_to_async
    def _get_game(self, player):
        if player is None:
            return
        return Game.objects.filter(players__id=player.id).first()

    @database_sync_to_async
    def _get_players_count(self, game):
        if game is None:
            return
        return Game.objects.get(id=game.id).players.count()

    @database_sync_to_async
    def _get_game_players_ids(self, game):
        if game is None:
            return
        players = game.players.all()
        return [player.id for player in players]

    @database_sync_to_async
    def _get_player_from_id(self, player_id):
        if player_id is None:
            return
        return Player.objects.get(id=player_id)

    async def connect(self):
        player = self.scope['player']
        game = self.scope['game']

        try:
            self.game_group_name = f'room_{str(game.id)}'
            await self.channel_layer.group_add(
                group=self.game_group_name,
                channel=self.channel_name,
            )

        except Exception as e:
            # ToDo: Add logging
            print('an error occurred: ', e)
            raise

        player_value = 'playerOne' if game.player_one_id == player.id else 'playerTwo'

        if game.started is False:
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'room.created',
                'text': 'Game room created',
                'player_id': str(player.id),
                'player_name': player.username,
                'player_value': player_value,
            })
        else:
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'room.joined',
                'text': f'Game room {self.game_group_name} joined',
                'player_id': str(player.id),
                'player_name': player.username,
                'player_value': player_value,
            })

        await self.accept()

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive_json(self, content, **kwargs):
        player_id = content.get('player_id')
        player = await self._get_player_from_id(player_id)
        if player is None:
            await self.close()
            return

        content['player_name'] = player.username
        message_type = content.get('type')
        if message_type == 'room.created':
            await self.room_created(content)
        elif message_type == 'room.joined':
            await self.room_joined(content)
        elif message_type == 'echo.message':
            await self.echo_message(content)
        elif message_type == 'chat.message':
            await self.channel_layer.group_send(
                self.game_group_name,
                content
            )
        elif message_type == 'game.move':
            await self.channel_layer.group_send(
                self.game_group_name,
                content
            )

    async def room_created(self, message):
        await self.send_json(message)

    async def room_joined(self, message):
        await self.send_json(message)

    async def echo_message(self, message):
        await self.send_json(message)

    async def chat_message(self, message):
        await self.send_json(message)

    async def game_move(self, message):
        await self.send_json(message)

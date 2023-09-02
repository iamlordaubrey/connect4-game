from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from game.models import Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name = None

    @database_sync_to_async
    def _get_game_id(self, player):
        if player is None:
            return
        return Game.objects.filter(players__id=player.id).first()

    async def connect(self):
        player = self.scope['player']
        if player is None:
            await self.close()

        game = await self._get_game_id(player)
        if game is None:
            await self.close()
            return

        try:
            self.game_group_name = f'room_{str(game.id)}'
            await self.channel_layer.group_add(
                group=self.game_group_name,
                channel=self.channel_name,
            )
            await self.channel_layer.group_send(self.game_group_name, {
                'type': 'room.created',
                'text': 'Game room created',
            })
        except Exception as e:
            print('an error occurred: ', e)
            raise

        await self.accept()

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')

        if message_type == 'room.created':
            await self.room_created(content)
        elif message_type == 'room.joined':
            await self.room_joined(content)
        elif message_type == 'echo.message':
            await self.send_json(content)

    async def room_created(self, message):
        await self.send_json(message)

    async def room_joined(self, message):
        await self.send_json(message)

    async def echo_message(self, message):
        await self.send_json(message)
import json

from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer, JsonWebsocketConsumer


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('bawo ni??', self.scope)
        player = self.scope['player']
        print('player in connect: ', player)
        if player is None:
            await self.close()
        else:
            await self.channel_layer.group_add(
                group='test',
                channel=self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'echo.message':
            await self.send_json({
                'type': message_type,
                'data': content.get('data'),
            })

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data'),
        })
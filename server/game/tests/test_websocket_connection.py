import pytest
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.test import Client
from rest_framework.reverse import reverse

from core.asgi import application
from player.models import Player

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@database_sync_to_async
# @pytest.mark.django_db(transaction=True)
def create_player(username):
    return Player.objects.create(username=username)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    @staticmethod
    def join_room(access_token):
        client = Client()
        return client.post(reverse('join_room'), **{'HTTP_player-id': access_token})

    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        player = await create_player('test.user@example.com')
        await sync_to_async(self.join_room)(player.id)

        communicator = WebsocketCommunicator(
            application=application,
            # path=f'/game/?player-id={str(player.id)}'
            path=f'/ws/socket-server/?player-id={str(player.id)}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        player = await create_player('test.user@example.com')
        await sync_to_async(self.join_room)(player.id)

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/socket-server/?player-id={str(player.id)}'
        )
        connected, _ = await communicator.connect()

        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)  # handles the BC sent on event type room.created

        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        player = await create_player('test.user@example.com')
        response = await sync_to_async(self.join_room)(player.id)
        game = response.data

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/socket-server/?player-id={str(player.id)}'
        )
        connected, _ = await communicator.connect()

        message = {
            'type': 'echo.message',
            'text': 'This is a test message.',
        }
        await communicator.send_json_to(message)  # handles the BC sent on event type room.created

        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'room_{str(game["id"])}', message=message)

        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

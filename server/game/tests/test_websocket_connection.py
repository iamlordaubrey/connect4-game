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

        payload = {
            'type': 'echo.message',
            'player': str(player.id),
            'message': 'This is a test message.',
        }
        await communicator.send_json_to(payload)  # handles the BC sent on event type room.created

        control_response = {
            'type': 'echo.message',
            'player': player.username,
            'message': 'This is a test message.',
        }
        server_response = await communicator.receive_json_from()

        assert control_response == server_response
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

        payload = {
            'type': 'echo.message',
            'player': str(player.id),
            'message': 'This is a test message.',
        }
        await communicator.send_json_to(payload)  # handles the BC sent on event type room.created

        channel_layer = get_channel_layer()
        await channel_layer.group_send(f'room_{str(game["id"])}', message=payload)

        control_response = {
            'type': 'echo.message',
            'player': player.username,
            'message': 'This is a test message.',
        }
        server_response = await communicator.receive_json_from()

        assert control_response == server_response
        await communicator.disconnect()

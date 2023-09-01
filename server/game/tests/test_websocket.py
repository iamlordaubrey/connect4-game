import pytest
from channels.db import SyncToAsync
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator

from core.asgi import application
from player.models import Player


@database_sync_to_async
@pytest.mark.django_db(transaction=True)
def create_player(username):
    player = Player.objects.create(
        username=username
    )
    access = player.id
    print('Wawuuuu', Player.objects.all())
    return player, access


@database_sync_to_async
@pytest.mark.django_db(transaction=True)
def get_player(access):
    return Player.objects.get(id=access)


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebSocket:
    async def test_can_connect_to_server(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_player(
            'test.user@example.com'
        )

        print('do we get here in test??', access, type(str(access)))
        print('in test, all players, ', await get_player(access))
        communicator = WebsocketCommunicator(
            application=application,
            path=f'/game/?player-id={str(access)}'
        )
        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_receive_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_player(
            'test.user@example.com'
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/game/?player-id={str(access)}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_receive_broadcast_messages(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = await create_player(
            'test.user@example.com'
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/game/?player-id={str(access)}'
        )
        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message.',
        }
        channel_layer = get_channel_layer()
        await channel_layer.group_send('test', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    # async def test_closes_things(self):
    #     assert 1 == 1


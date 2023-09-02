import pytest
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import Client
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APITransactionTestCase

from core.asgi import application
from game.models import Game
from player.models import Player

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


def create_player(username):
    return Player.objects.create(username=username)


class TestGameRoom(APITestCase):
    def test_first_player_joins_game_room_creates_room(self):
        player = create_player('test.user@example.com')
        response = self.client.post(reverse('join_room'), **{'HTTP_player-id': player.id})

        game = Game.objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], str(game.id))
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['id'], str(player.id))
        self.assertEqual(response.data['started'], False)

    def test_second_player_joining_game_room_joins_existing_room(self):
        player1 = Player.objects.create(username='test_user_1')

        """
        Bypassing the serializer here. Creating game_room directly on the database and 
        adding player1 to the game_room
        """
        game_room1 = Game.objects.create()
        game_rooms_queryset1 = Game.objects.all()
        game_room1.players.add(player1)

        self.assertEqual(len(game_rooms_queryset1), 1)
        self.assertEqual(game_room1.started, False)

        player2 = Player.objects.create(username='test_user_2')

        """
        Need to go through the serializer here. Hitting the game Serializer should add 
        player2 to the already existing game_room 
        """
        response = self.client.post(reverse('join_room'), **{'HTTP_player-id': player2.id})
        game_room2 = response.data
        game_rooms_queryset2 = Game.objects.all()

        self.assertEqual(len(game_rooms_queryset2), 1)
        self.assertEqual(str(game_room1.id), game_room2['id'])
        self.assertEqual(game_room2['started'], True)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestJoiningGameRoomCreatesWebsocketConnection(APITransactionTestCase):
    @staticmethod
    def join_room(access_token):
        client = Client()
        return client.post(reverse('join_room'), **{'HTTP_player-id': access_token})

    async def test_player_creates_room_and_receives_broadcast_message(self):
        player = await database_sync_to_async(create_player)('test_user')
        await sync_to_async(self.join_room)(player.id)

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/ws/socket-server/?player-id={str(player.id)}'
        )
        connected, _ = await communicator.connect()
        assert connected is True

        message = {
            'type': 'room.created',
            'text': 'Game room created',
        }
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

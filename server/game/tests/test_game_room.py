import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from core.asgi import application
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APITransactionTestCase

from game.models import Game
from player.models import Player


# @database_sync_to_async
# @pytest.mark.django_db(transaction=True)
def create_player(username):
    print('in create player func')
    return Player.objects.create(
        username=username
    )
    # access = player.id
    # return player


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


class TestGameRoom(APITestCase):
    def test_first_player_joins_game_room_creates_room(self):
        print('about to run..')
        # settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        player = create_player('test.user@example.com')
        #
        # communicator = WebsocketCommunicator(
        #     application=application,
        #     path=f'/game/?player-id={str(access)}'
        # )
        # connected, _ = await communicator.connect()

        response = self.client.post(reverse('join_room'), **{'HTTP_player-id': player.id})
        print('response: ', response)
        player = Player.objects.last()
        print('player: ', player)

        game = Game.objects.last()
        print('game: ', game)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], str(game.id))
        self.assertEqual(len(response.data['players']), 1)
        self.assertEqual(response.data['players'][0]['id'], str(player.id))
        self.assertEqual(response.data['started'], False)

        # assert connected is True
        # await communicator.disconnect()

    def test_second_player_joining_game_room_joins_existing_room(self):
        player1 = Player.objects.create(username='test_user_1')
        print('player1', player1)
        # Bypassing the serializer here, creating directly on the database
        """
        Bypassing the serializer here. Creating game_room directly on the database and 
        adding player1 to the game_room
        """
        game_room1 = Game.objects.create()
        game_rooms_queryset1 = Game.objects.all()
        game_room1.players.add(player1)
        print('game_room1', game_room1)

        self.assertEqual(len(game_rooms_queryset1), 1)
        self.assertEqual(game_room1.started, False)

        player2 = Player.objects.create(username='test_user_2')
        print('p1, p2', player1, player2)
        # Need to go through the serializer here. Hitting the endpoint
        """
        Need to go through the serializer here. Hitting the game_room endpoint
        Serializer should join the game_room and add player2 to the game_room 
        """
        response = self.client.post(reverse('join_room'), **{'HTTP_player-id': player2.id})
        game_room2 = response.data
        # game_room2 = Game.objects.create()
        game_rooms_queryset2 = Game.objects.all()
        # game_room2.players.add(player2)
        print('g1', game_room1, 'g2', game_room2)
        print('g1.started', game_room1.started, 'g2.started', game_room2['started'])

        self.assertEqual(len(game_rooms_queryset2), 1)
        self.assertEqual(str(game_room1.id), game_room2['id'])
        self.assertEqual(game_room2['started'], True)


from asgiref.sync import sync_to_async
from django.test import Client


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestJoiningGameRoomCreatesWebsocketConnection(APITransactionTestCase):
    # @database_sync_to_async
    # def create_guy(self, user):
    #     return Player.objects.create(username=user)

    def join_room(self, access_token):
        client = Client()
        return client.post(reverse('join_room'), **{'HTTP_player-id': access_token})

    # @sync_to_async
    # def create_player_and_join_room(self):
    #     player, access = create_player(username='test_user_1')
    #     response = client.post(reverse('join_room'), **{'HTTP_player-id': access})
    #
    #     print('response: ', response)
    #     return player, access, response.data

    async def test_player1_creates_room_and_receives_broadcast_message(self):
        # player0 = await self.create_guy('username')
        player = await database_sync_to_async(create_player)('test_user_0')
        response = await sync_to_async(self.join_room)(player.id)
        game = response.data

        communicator = WebsocketCommunicator(
            application=application,
            path=f'/game/?player-id={str(player.id)}'
        )
        connected, _ = await communicator.connect()
        assert connected is True

        message = {
            'type': 'room.created',
            'text': 'Game room created',
        }

        response = await communicator.receive_json_from()
        print('response from receive', response)
        assert response == message
        await communicator.disconnect()

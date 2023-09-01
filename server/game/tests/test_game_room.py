import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from core.asgi import application
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from game.models import Game
from player.models import Player


# @database_sync_to_async
# @pytest.mark.django_db(transaction=True)
def create_player(username):
    print('in create player func')
    player = Player.objects.create(
        username=username
    )
    access = player.id
    return player, access


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


class TestGameRoom(APITestCase):
    def test_first_player_joins_game_room_creates_room(self):
        print('about to run..')
        # settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        _, access = create_player('test.user@example.com')
        #
        # communicator = WebsocketCommunicator(
        #     application=application,
        #     path=f'/game/?player-id={str(access)}'
        # )
        # connected, _ = await communicator.connect()

        response = self.client.post(reverse('join_room'), **{'HTTP_player-id': access})
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
        print('g1, g2', game_room1, game_room2)

        self.assertEqual(len(game_rooms_queryset2), 1)
        self.assertEqual(str(game_room1.id), game_room2['id'])
        self.assertEqual(game_room1.started, True)


# class TestPlayerTest2(APITestCase):
#     def test_user_can_create_player(self):
#         print('yahoo!')
#         self.assertEqual(1+2, 7)
#         # username = 'test_player'
#         # response = self.client.post(reverse('create_player'), data={
#         #     'username': username
#         # })
#         # player = Player.objects.last()
#         # self.assertEqual(status.HTTP_201_CREATED, response.status_code)
#         # self.assertEqual(response.data['id'], str(player.id))
#         # self.assertEqual(response.data['username'], player.username)
#         # self.assertEqual(response.data['wins'], player.wins)
#         # self.assertEqual(response.data['losses'], player.losses)

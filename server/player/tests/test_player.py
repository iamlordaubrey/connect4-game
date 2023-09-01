from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from player.models import Player


class TestPlayer(APITestCase):
    def test_user_can_create_player(self):
        username = 'test_player'
        response = self.client.post(reverse('create_player'), data={
            'username': username
        })
        player = Player.objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], str(player.id))
        self.assertEqual(response.data['username'], player.username)
        self.assertEqual(response.data['wins'], player.wins)
        self.assertEqual(response.data['losses'], player.losses)

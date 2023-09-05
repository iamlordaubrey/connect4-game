from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.db import close_old_connections

from game.models import Game
from player.models import Player


@database_sync_to_async
def get_player(player_id):
    return Player.objects.get(id=player_id)


@database_sync_to_async
def get_game(game_id):
    return Game.objects.get(id=game_id)


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = parse_qs(scope['query_string'].decode())
        token_list = query_string.get('player-id')
        game_list = query_string.get('game-id')
        if not token_list and game_list:
            scope['player'] = None
            scope['game'] = None
            return await self.app(scope, receive, send)

        token = token_list[0]
        game = game_list[0]
        try:
            player = await get_player(token)
            game = await get_game(game)
        except Exception as exception:
            print('An error occurred: ', exception)
            scope['player'] = None
            scope['game'] = None
            return await self.app(scope, receive, send)

        scope['player'] = player
        scope['game'] = game
        return await self.app(scope, receive, send)

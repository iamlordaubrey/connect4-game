from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.db import close_old_connections

from player.models import Player


@database_sync_to_async
def get_player(player_id):
    return Player.objects.get(id=player_id)


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = parse_qs(scope['query_string'].decode())
        token_list = query_string.get('player-id')
        if not token_list:
            scope['player'] = None
            return await self.app(scope, receive, send)

        token = token_list[0]
        try:
            player = await get_player(token)
        except Exception as exception:
            print('An error occurred: ', exception)
            scope['player'] = None
            return await self.app(scope, receive, send)

        scope['player'] = player
        return await self.app(scope, receive, send)

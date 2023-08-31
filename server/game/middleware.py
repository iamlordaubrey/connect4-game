import uuid
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.db import close_old_connections

from player.models import Player


@database_sync_to_async
def get_player(player_id):
    return Player.objects.get(id=player_id)


    # print('player id: ', player_id)
    # player_uuid = uuid.UUID(player_id)
    # # player_id = player_id.decode('utf-8')
    # print('we should get here', player_uuid, type(player_uuid))
    # print('all players: ', Player.objects.all(), ' the end')
    # returned_player = Player.objects.get(id=player_id)
    # print('returned player: ', returned_player)
    # return returned_player


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        print(scope['query_string'])
        # query_string = parse_qs(scope['query_string'].decode())
        query_string = parse_qs(scope['query_string'].decode())
        print('qs: ', query_string)
        token = query_string.get('player-id')[0]
        print('in call token: ', token)
        if not token:
            scope['player'] = None
            return await self.app(scope, receive, send)

        try:
            player = get_player(token)
        except Exception as exception:
            scope['player'] = None
            return await self.app(scope, receive, send)

        scope['player'] = player
        return await self.app(scope, receive, send)

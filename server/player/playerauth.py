from channels.db import database_sync_to_async

from player.models import Player


@database_sync_to_async
def get_player(player_id):
    return Player.objects.get(id=player_id.decode('utf-8'))


class PlayerAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope['player'] = await get_player(scope['query_string'])
        return await self.app(scope, receive, send)

# import uuid
# from urllib.parse import parse_qs
#
# from channels.db import database_sync_to_async
# from django.db import close_old_connections
#
# from player.models import Player
#
#
# # @database_sync_to_async
# def get_player(player_id):
#     print('player id: ', player_id)
#     player_id = uuid.UUID(player_id)
#     # player_id = player_id.decode('utf-8')
#     print('we should get here', player_id, type(player_id))
#     return Player.objects.get(id=player_id)
#
#
# class PlayerTokenAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, scope, *args, **kwargs):
#         close_old_connections()
#         query_string = parse_qs(scope['query_string'])
#         token = query_string.get('player-id')
#         if not token:
#             scope['player'] = None
#             return self.get_response(scope)
#
#         try:
#             player = get_player(token)
#         except Exception as exception:
#             scope['player'] = None
#             return self.get_response(scope)
#
#         scope['player'] = player
#         return self.get_response(scope)
#
#
#     # def __init__(self, app):
#     #     self.app = app
#     #
#     # async def __call__(self, scope, receive, send):
#     #     scope['player'] = await get_player(scope['query_string'])
#     #
#     #     print('do we get here?')
#     #     return await self.app(scope, receive, send)

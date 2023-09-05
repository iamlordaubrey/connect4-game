import uuid

from django.db import models


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    players = models.ManyToManyField('player.Player')
    player_one = models.ForeignKey("player.Player", on_delete=models.SET_NULL, blank=True, null=True, related_name='player_one')
    player_two = models.ForeignKey("player.Player", on_delete=models.SET_NULL, blank=True, null=True, related_name='player_two')
    started = models.BooleanField(default=False)

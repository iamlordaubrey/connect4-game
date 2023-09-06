import uuid

from django.db import models


class Player(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=48, unique=True)
    wins = models.IntegerField(default=0, blank=True)
    losses = models.IntegerField(default=0, blank=True)

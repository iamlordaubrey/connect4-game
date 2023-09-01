from django.urls import path

from player.views import CreatePlayerView

urlpatterns = [
    path('create/', CreatePlayerView.as_view(), name='create_player'),
]

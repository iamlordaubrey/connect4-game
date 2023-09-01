from django.urls import path

from game.views import JoinRoomView

urlpatterns = [
    path('join/', JoinRoomView.as_view(), name='join_room'),
]

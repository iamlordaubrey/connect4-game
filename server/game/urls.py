from django.urls import path

from game.views import JoinView

urlpatterns = [
    path('join/', JoinView.as_view()),
]
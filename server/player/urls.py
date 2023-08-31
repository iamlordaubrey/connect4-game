from django.urls import path

from player.views import CreateView

urlpatterns = [
    path('create/', CreateView.as_view()),
]

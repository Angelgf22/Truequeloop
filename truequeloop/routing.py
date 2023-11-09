from django.urls import path, re_path

from apps.truequeloop_app import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:uuid>/', consumers.ChatConsumer.as_asgi()),
]

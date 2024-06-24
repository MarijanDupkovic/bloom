from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('screen_capture/', consumers.ScreenCaptureConsumer),
]
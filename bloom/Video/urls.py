from . import consumers
from django.urls import path


websocket_urlpatterns = [
    path('screen_capture/', consumers.ScreenCaptureConsumer),
]
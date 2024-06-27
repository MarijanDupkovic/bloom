from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import VideoItem
from .serializers import VideoItemSerializer
from rest_framework.authentication import TokenAuthentication
from django.core.cache import cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = VideoItemSerializer
    queryset = VideoItem.objects.all()
  
    def get_queryset(self):

     queryset = cache.get('videoList')
     if not queryset:
           queryset = VideoItem.objects.all()
           cache.set('videoList', queryset, CACHE_TTL)

     return queryset



    
def video_by_token(request, token):
      video = get_object_or_404(VideoItem, access_token=token)
      return HttpResponse(f"Video: {video.id}")
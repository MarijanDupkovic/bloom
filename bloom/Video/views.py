import os
import re
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




from django.http import StreamingHttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import VideoItem

def video_by_token(request, token):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    video = get_object_or_404(VideoItem, access_token=token)
    try:
        video_file_path = video.video_file_apple.path if 'iphone' in user_agent or 'ipad' in user_agent or ('safari' in user_agent and not 'chrome' in user_agent) else video.video_file.path 
        def stream_video(video_path, start=None, end=None):
            with open(video_path, 'rb') as video_file:
                if start:
                    video_file.seek(start)
                while True:
                    bytes_to_read = min(8192, end - video_file.tell() + 1) if end else 8192
                    chunk = video_file.read(bytes_to_read)
                    if not chunk:
                        break
                    yield chunk

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        size = os.path.getsize(video_file_path)
        content_type = 'video/mp4'
        if range_match:
            start, end = range_match.groups()
            start = int(start)
            end = int(end) if end else size - 1
            response = StreamingHttpResponse(stream_video(video_file_path, start, end), status=206, content_type=content_type)
            response['Content-Range'] = f'bytes {start}-{end}/{size}'
        else:
            response = StreamingHttpResponse(stream_video(video_file_path), content_type=content_type)
        response['Accept-Ranges'] = 'bytes'
        response['Content-Length'] = str(size if not range_match else end - start + 1)
        response['Content-Disposition'] = 'inline; filename="video.mp4"'
        return response
    except AttributeError:
        raise Http404("Video file not found.")
    

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        video_data = request.body
        video_path = os.path.join('liveTest', 'live_stream.mp4')

        with open(video_path, 'ab') as f:
            f.write(video_data)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
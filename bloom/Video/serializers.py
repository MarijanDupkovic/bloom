from rest_framework import serializers
from .models import VideoItem

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoItem
        fields = ('id','title','author','video_file','video_file_1080p','created_at')
       
    
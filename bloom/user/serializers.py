from rest_framework import serializers
from Video.serializers import VideoItemSerializer

from user.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    videoitem_set = VideoItemSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','profile_picture','videoitem_set']
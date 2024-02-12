from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from user.models import CustomUser

@api_view(('put',))
def change_profile_img(request, token):
    user = get_object_or_404(CustomUser, auth_token=token)
    user.profile_picture = request.fields.get('profile_picture')
    user.save()
    return Response({'message': 'Profile picture updated successfully!'})
import uuid
from django.db import models
import datetime
from django.utils.translation import gettext as _
from user.models import CustomUser

class VideoItem(models.Model):
    title = models.CharField(max_length=100,blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(_("Created At"), default=datetime.date.today)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_1080p = models.FileField(upload_to='videos', blank=True, null=True)
    access_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.title:
           self.title = f'_{uuid.uuid4()}'
        super().save(*args, **kwargs)

    
    

   

   
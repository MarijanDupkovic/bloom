import uuid
from django.db import models
import datetime
from django.utils.translation import gettext as _

from user.models import CustomUser

    
class VideoItem(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(_("Created At"), default=datetime.date.today)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_1080p = models.FileField(upload_to='videos', blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}. |  {self.title}'

    def generate_unique_title(self, username):
        unique_title = f'{username}_{uuid.uuid4()}'
        if VideoItem.objects.filter(title=unique_title).exists():
            return self.generate_unique_title(username)
        return unique_title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.generate_unique_title(self.author.username)
        super().save(*args, **kwargs)
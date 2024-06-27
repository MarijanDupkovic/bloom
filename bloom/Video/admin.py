from django.contrib import admin
from import_export import resources
from .models import VideoItem
from import_export.admin import ImportExportModelAdmin

class VideoItemRessource(resources.ModelResource):
    class Meta:
        model = VideoItem
        


@admin.register(VideoItem)
class VideoAdmin(ImportExportModelAdmin):
    list_display = ('id','title','author','video_file','video_file_1080p','created_at','access_token')



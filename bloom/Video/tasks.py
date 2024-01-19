import os
import subprocess

from Video.models import VideoItem
   
def convert_1080p(source):
    new_file_name = source.split('.')[0] + '_1080p.mp4' 
    file_name = os.path.basename(source)

    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.Popen(cmd,shell=True)
    run.wait()

    video = VideoItem.objects.get(video_file__icontains=file_name) 
    new_path = 'videos/{}'.format(os.path.basename(new_file_name))
    video.video_file_1080p = new_path
    video.save()
    print("Converting to 1080px finished!")
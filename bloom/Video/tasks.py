import os
import subprocess

from Video.models import VideoItem
   
def convert_1080p(source):
    new_file_name = source.split('.')[0] + '_1080p.mp4' 
    file_name = os.path.basename(source)

    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    run = subprocess.Popen(cmd,shell=True)
    run.wait()

    video = VideoItem.objects.get(video_file__icontains=file_name) 
    new_path = 'videos/{}'.format(os.path.basename(new_file_name))
    video.video_file_1080p = new_path
    video.save()

    print("Converting to 1080px finished!")


def convert_apple(source):
    new_file_name = os.path.splitext(source)[0] + '_apple.mp4'
    file_name = os.path.basename(source)

    cmd = 'ffmpeg -i "{}" -c:v libx264 -preset ultrafast -profile:v main -level 3.0 -c:a aac -strict experimental -b:a 256k "{}"'.format(source, new_file_name)
    
    try:
        run = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = run.communicate()
        if run.returncode != 0:
            print("Error converting video: ", error)
            return
    except Exception as e:
        print("Exception occurred: ", e)
        return

    video = VideoItem.objects.get(video_file__icontains=file_name)
    new_path = 'videos/{}'.format(os.path.basename(new_file_name))
    
    video.video_file_apple = new_path
    video.save()

    print("Converting to apple finished!")
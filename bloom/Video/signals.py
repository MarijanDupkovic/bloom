from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os
import django_rq
from .tasks import convert_1080p, convert_apple
from .models import VideoItem
from django.core.cache import cache

@receiver(post_save, sender=VideoItem)
def video_post_save(sender, instance, created, **kwargs):
    print("Video saved!")
    if created:
        print('New video created')
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_apple,instance.video_file.path)
        #queue.enqueue(convert_1080p,instance.video_file.path)

        cache.delete_many(keys=cache.keys('*videoList*'))

@receiver(post_delete, sender=VideoItem)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(os.remove,instance.video_file.path)
            print("Video file deleted!")
            
            
            queue.enqueue(os.remove,instance.video_file.path.split('.')[0] + '_1080p.mp4')
            print("Video file @1080p deleted!")

            queue.enqueue(os.remove,instance.video_file.path.split('.')[0] + '_apple.mp4')
            print("Video file apple deleted!")


        else: print("No video file found")
    cache.delete_many(keys=cache.keys('*videoList*'))
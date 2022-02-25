from __future__ import absolute_import, unicode_literals
from django.http import FileResponse
from celery import shared_task
from moviepy.editor import VideoFileClip
import os
from Youtube_to_MP3_converter.celery import app
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
        CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@shared_task
def mp4_to_mp3(mp4_file,title):
    mp3_file = title + ".mp3"
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoclip.close()
    os.remove(mp4_file)
    print(os.path.normpath(mp3_file))
    return mp3_file
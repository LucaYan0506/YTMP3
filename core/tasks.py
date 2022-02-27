from __future__ import absolute_import, unicode_literals
from celery import shared_task
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os
from .models import Song_data

from Youtube_to_MP3_converter.celery import app
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
        CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@shared_task
def mp4_to_mp3(link,id):
    yt = YouTube(link)
    streams = yt.streams.filter()
    stream= streams.first()
    mp4_file=stream.download(skip_existing=True)
    mp3_file = str(id) + ".mp3"
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoclip.close()
    path=os.path.normpath(mp3_file)
    with open(path,'rb') as f:
        byteData=f.read()
    
    new_song = Song_data.objects.get(pk = id)
    new_song.record = byteData
    new_song.download_complete = True
    new_song.save()

    os.remove(mp3_file)
    os.remove(mp4_file)

    return 0
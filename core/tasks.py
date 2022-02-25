from __future__ import absolute_import, unicode_literals
from django.http import FileResponse
from celery import shared_task
from moviepy.editor import VideoFileClip
import os

@shared_task
def mp4_to_mp3(mp4_file,title):
    mp3_file = title + ".mp3"
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    audioclip.close()
    videoclip.close()
    os.remove(mp4_file)
    return mp3_file
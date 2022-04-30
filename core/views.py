from django.shortcuts import render
from django.urls.base import reverse
from django.http import HttpResponseRedirect,FileResponse,JsonResponse
from pytubeCustom import YouTube
from .tasks import mp4_to_mp3
from .models import Song_data
from io import BytesIO
import os

# Create your views here.

def index_view(request):
    lang = request.GET.get('lang')
    if lang == 'ZH':
        return render(request,'index.html')
    elif lang == 'IT':
        return render(request,'IT.html')

    return render(request,'EN.html')

def convert(request):
    if request.method == "POST":
        lang = request.POST['lan']
        yt = ""
        try:
            yt = YouTube(request.POST['link'])
            yt.check_availability()
        except:
            if lang == 'ZH':
                return render(request,'index.html',{
                    'message':'未找到网页'
                })
            elif lang == 'IT':
                return render(request,'IT.html',{
                    'message':'Url invalido'
                })
            else:
                return render(request,'EN.html',{
                    'message':'Invalid url'
                })
        
        new_song = Song_data(title=yt.title)
        new_song.save()
        mp4_to_mp3.delay(request.POST['link'],new_song.pk)
        if lang == 'ZH':
            return render(request,'converting_en.html',{
                'id':new_song.pk,
                'lang': '中文',
                'lan': 'ZH',
                'h1': '转换中...',
                'complete': '转换完成',
                'p': "请不要关闭或刷新这个网页",
                'a': '再下载一个',
            })
        elif lang == 'IT':
            return render(request,'converting_en.html',{
                'id':new_song.pk,
                'lan': 'IT',
                'lang': 'Italiano',
                'complete': 'Conversione completato',
                'h1': 'sta convertendo...',
                'p': "Non chiudere o ricaricare questa pagina ",
                'a': 'Scarica un altro',
            })
        else:
            return render(request,'converting_en.html',{
                'id':new_song.pk,
                'lan': 'EN',
                'lang': 'English',
                'h1': 'Converting...',
                'complete': 'Conversion completed',
                'p': "Please don't close or reload this page",
                'a': 'Download another one',
            })
    
    return JsonResponse({'message':'Invalid URL'},safe=False)

#bug: if 2 users are downloading the same file one of them may not receive the file
def download(request):
    song = Song_data.objects.get(pk = request.GET.get('id'))
    if song.download_complete == True:
        byteData = song.record
        return FileResponse(BytesIO(byteData),filename=song.title + ".mp3",as_attachment=True,content_type='audio/mpeg')

    return JsonResponse({'message':'wait please'},safe=False)

def check_task(request):
    return JsonResponse({'exists': Song_data.objects.get(pk = request.GET.get('id')).download_complete},safe=False)
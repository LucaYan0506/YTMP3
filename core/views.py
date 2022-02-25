from django.shortcuts import render
from django.urls.base import reverse
from django.http import HttpResponseRedirect,FileResponse,JsonResponse
from pytube import YouTube
from .tasks import mp4_to_mp3
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
        
        streams = yt.streams.filter()
        stream= streams.first()
        data=stream.download(skip_existing=True)
        mp4_to_mp3.delay(data,yt.title)
        if lang == 'ZH':
            return render(request,'converting_en.html',{
                'title':yt.title,
                'lang': '中文',
                'lan': 'ZH',
                'h1': '转换中...',
                'complete': '转换完成',
                'p': "请不要关闭或刷新这个网页",
                'a': '再下载一个',
            })
        elif lang == 'IT':
            return render(request,'converting_en.html',{
                'title':yt.title,
                'lan': 'IT',
                'lang': 'Italiano',
                'complete': 'Conversione completato',
                'h1': 'sta convertendo...',
                'p': "Non chiudere o ricaricare questa pagina ",
                'a': 'Scarica un altro',
            })
        else:
            return render(request,'converting_en.html',{
                'title':yt.title,
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
    title = request.GET.get('title') + ".mp3"
    if title != '':
        path=os.path.normpath(title)
        with open(path,'rb') as f:
            byteData=f.read()
        os.remove(title)
        return FileResponse(BytesIO(byteData),filename=title,as_attachment=True,content_type='audio/mpeg')

    return JsonResponse({'message':'wait please'},safe=False)

def check_task(request):
    return JsonResponse({'exists':os.path.exists(request.GET.get('title') + ".mp3")},safe=False)
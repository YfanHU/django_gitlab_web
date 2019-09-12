from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from gitlab_web.utils import qqmusic_utils
from xpinyin import Pinyin

def index(request):
    return render(request,'qqmusic_download/index.html')


def download_music(request):
    if request.method == 'POST':
        print(request.POST)
        songname = request.POST['songname']
        format = request.POST['format']
        download = True if request.POST['method']=='offline' else False
        success,info=qqmusic_utils.download_song(songname,format,download)
        if success:
            if download:
                f = open(info, 'rb')
                # msg = f.read()
                response = FileResponse(f)
                response['Content-Type'] = 'application/octet-stream'
                Pinyin().get_pinyin()
                print('Content-Disposition:','attachment;filename="{}"'.format(Pinyin().get_pinyin(info.split('/')[-1])))
                response['Content-Disposition'] = 'attachment;filename="{}"'.format(Pinyin().get_pinyin(info.split('/')[-1]))
                return response
            else :
                return redirect(info)
        else :
            return render(request, 'qqmusic_download/index.html',context={'warn_msg':info})
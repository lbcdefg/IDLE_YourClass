from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from django.shortcuts import redirect
from ..forms import PostWriteForm 
from django.utils import timezone

# 자료실에서 파일 업로드와 글쓰기
def post_write(request):
    category_name = '자료실'
    context = {
            'category_name' : category_name,
        }
    if request.method == "POST":
        form = PostWriteForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(**form.cleaned_data)
            nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            post.date = nowDatetime
            post.category = Categories.objects.get(Cat_name="자료실")
            post.author = Member.objects.get(email=request.session['login_'])
            if request.FILES:
                print("request.FILES 있음")
                if 'file' in request.FILES.keys():
                    post.filename = request.FILES['file'].name
            post.save()
            return redirect('board_category', '자료실')
    else:
        form = PostWriteForm()
    context = {
        'form' : form
    }
    return render(request, 'createPost.html', context)

import urllib
import os
from django.http import Http404
import mimetypes
from django.shortcuts import get_object_or_404

# 다운로드 기능
def post_download(request, pk):
    post = get_object_or_404(Post, pk=pk)
    url = post.file.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(post.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
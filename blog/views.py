from django.shortcuts import render,get_object_or_404,render_to_response,redirect
from django.http import HttpResponse
from .models import Post,Category,Tag,Tools
import markdown
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import os

# Create your views here.
def index(request):
    post_list=Post.objects.all()
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'blog/index.html',context={'post_list':post_list})

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.increase_views()
    md=markdown.Markdown(extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                     TocExtension(slugify=slugify),
                                ])
    post.body=md.convert(post.body)
    post.toc=md.toc
    ##控制文章目录是否显示
    if post.toc.find('<li>')==-1:
        post.toc=""
    print('toc: '+str(post.toc))
    form=CommentForm()
    comment_list = post.comment_set.all()

    paginator = Paginator(comment_list, 2)
    page = request.GET.get('page')

    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)


    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request,pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', context={'post_list': post_list})

def tools(request):
    tool_list = Tools.objects.all()
    return render(request,'blog/tools.html',context={'tool_list':tool_list})

def toolname(request,tool_name):
    tool=Tools.objects.get(name=tool_name)
    return render(request,'blog/tools/'+tool_name+'.html',context={'tool':tool})

def video(request):
    video_list=[]
    for videoname in os.listdir(r'F:\\test'):
        if videoname.split('.')[-1] == 'mp4':
            video_list.append(videoname.split('.')[0])
    return render(request,'blog/video.html',context={'video_list':video_list})

def videoname(request,video_name):
    url='http://192.168.0.100:8090/'+video_name+'.mp4'
    return redirect(url)

def test(request):
    return render(request,'blog/test.html')

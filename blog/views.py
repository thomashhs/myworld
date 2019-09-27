from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.
def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list, 2)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request,'blog/index.html',context={'post_list':post_list,
                                                     'paginator':paginator})

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
    form=CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request,pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request,pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
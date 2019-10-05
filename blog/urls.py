from django.conf.urls import url

from . import views
app_name = 'blog'

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),

    url(r'^tools/$', views.tools, name='tools'),
    url(r'^tools/(?P<tool_name>\w+)/$', views.toolname, name='toolname'),

    url(r'^video/$', views.video, name='video'),
    url(r'^video/(?P<video_name>\w+)/$', views.videoname, name='videoname'),

    url(r'^test/$', views.test, name='test'),

]
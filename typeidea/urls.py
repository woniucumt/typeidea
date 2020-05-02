"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import url,include
from .custom_site import custom_site
from django.views.generic import TemplateView

#from blog.views import post_detail,post_list
from blog.views import IndexView, CategoryView,TagView,PostDetailView, SearchView,aboumeView
from blog.views import acaindexView, testView, galleryView, BlogIndexView, postlistView
from blog.views import postdetialview,acaCTView,newindexView
from config.views import LinkListView
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

urlpatterns = [


    # url(r'^$',post_list),
    # url(r'^category/(?P<category_id>\d+)/$',post_list),
    # url(r'tag/(?P<tag_id>\d+)/$',post_list),
    # url(r'^post/(?P<post_id>\d+).html$',post_detail),
    # url(r'^links/$',links),
    # url(r'^admin/', custom_site.urls),
    # url(r'^super_admin/', admin.site.urls),
    url(r'^$',IndexView.as_view(),name='newIndex'),  #项目的总index
    url(r'^blogindex/', BlogIndexView.as_view(), name='blog-view'),  # 博客首页
    url(r'^about/', aboumeView.as_view(),name='aboutme'),#关于我
    url(r'^acaindex/', acaindexView.as_view(), name='academic-view'), #学术首页
    url(r'^gallery/', galleryView.as_view(), name='gallery-view'), #画廊首页

    #学术部分
    url(r'^acaCT/', acaCTView.as_view(), name='academic-CT'),

    #博客部分
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(),name='tag-list'),
    url(r'^postdetail/(?P<post_id>\d+).html/$', PostDetailView.as_view(),name='post-detail'),
    url(r'^postlist/', postlistView.as_view(), name='postlist'),
    # url(r'^details/$', postdetialview.as_view()),

    #设置部分
    # url(r'^admin/', custom_site.urls),
    url(r'^admin/', admin.site.urls),
    # url(r'^super_admin/', admin.site.urls),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^linkd/$',LinkListView.as_view(),name='links'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^test/', testView.as_view(),name='test-view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

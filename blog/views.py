from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tag, Post, Category
from config.models import SideBar
from django.views.generic import DetailView, ListView,TemplateView
from datetime import datetime
import os
import requests
import json
import pprint
from django.http import HttpResponse

# Create your views here.
#注意下面这三个参数。首先是request。url的作用就是分发request其实。于是request是发到这里的
#另外，注意这个view是两个地方用，于是就有了两个category_id 和 tag_id的
# def post_list(request,category_id=None, tag_id=None):
#     tag = None
#     category = Nonety
#
#     if tag_id:
#             post_list, tag = Post.get_by_tag(tag_id)
#     elif category_id:
#             post_list, category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#
#     return render(request, 'blog/list.html',context=context)

class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars':SideBar.get_all()})
        context.update(Category.get_navs())
        paginator_range = context["paginator"].page_range
        context.update({
            "paginator_range": paginator_range
        })
        addrString = ''
        # 查询ip的接口
        try:
            r = requests.get(url='http://whois.pconline.com.cn/ipJson.jsp?ip='+str(self.request.META.get('REMOTE_ADDR'))+'&json=true')
            print('http://whois.pconline.com.cn/ipJson.jsp?ip='+self.request.META.get('REMOTE_ADDR')+'&json=true')
            # print(type(json.loads(r.content)))
            jsonStr = json.loads(str(r.content, encoding="gbk"))
            # jsonStr = json.loads(str(r.content, encoding="utf-8"))
            # print(jsonStr["country"]+jsonStr["regionName"]+jsonStr["city"])
            # addrString = jsonStr["country"]+jsonStr["regionName"]+jsonStr["city"]
            addrString = jsonStr["addr"]
        except Exception as e:
            print(e)
        try:
            with open(os.path.dirname(os.path.abspath(__file__))+'visitRecord.txt', 'a') as f:
                f.write("IP："+self.request.META.get('REMOTE_ADDR')+"日期："+addrString+str(datetime.now())+"\n")
                f.close()
        except Exception as e:
            print(e)
        # print("IP：",self.request.META.get('REMOTE_ADDR'),"日期：",datetime.now())
        return context

# 为了部分页自己做的，这是很不好的方法。为了减少函数体，去除记录IP的方法。
class CommonViewMixinDetails:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sidebars':SideBar.get_all()})
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'newindex/newindex.html'

#index拆开了，就只好这样写了，前端不给力。
class IndexViewHome(TemplateView):
    template_name = 'newindex/index-home.html'
class IndexViewBlog(TemplateView):
    template_name = 'newindex/index-blog.html'
class IndexViewAca(TemplateView):
    template_name = 'newindex/index-aca.html'
class IndexViewGallery(TemplateView):
    template_name = 'newindex/index-gallery.html'

# beta版本的index的路由
# def index_diagoona (request, page_name):
#     page_name = page_name
#     return render(request,'newindex/index-'+page_name+'.html')


class BlogIndexView(IndexView):
    queryset = Post.latest_posts()
    paginate_by = 12
    context_object_name = 'post_list'
    template_name = 'blog/blogindex2.html'

class postlistView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 8
    context_object_name = 'post_list'
    template_name = 'blog/blogpostlist2.html'

class CategoryView(postlistView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category,
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

# 基于方法的view
# def post_detail(request, post_id=None):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post':post,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#         #其实这个东西这里还是很神奇的。
#         #render过来，url和这个模板不一定要名字相同啊。
#     return render(request,'blog/details.html',context={'post':post})

class PostDetailView(CommonViewMixinDetails,DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/blogdetails2.html'
    pk_url_kwarg = 'post_id'

# 写一个新的details页面
#暂时用不到了
# class PostDetailView2(IndexView):
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({'sidebars':SideBar.get_all()})
#         context.update(Category.get_navs())
#         post_id = self.kwargs.get('post_id')
#         print("zhzhz",post_id)
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         post_id = int(self.kwargs.get('post_id'))
#         print(queryset.filter(id=post_id))
#         return queryset.filter(id=post_id)
#     # queryset = Post.get_one_post()
#     context_object_name = 'posts'
#     template_name = 'blog/blogdetails2.html'

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

class aboumeView(IndexView):
    template_name = 'aboutME/aboutme2.html'

class abousiteView(IndexView):
    template_name = 'aboutME/aboutsite.html'

class acaindexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'acaindex/acaindex.html'

class testView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'test/test.html'

class galleryView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'gallery/galleryindex.html'


class postdetialview(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/blogdetails.html'
    pk_url_kwarg = 'post_id'

class acaCTView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'acaindex/acaCT.html'

class newindexView(CommonViewMixin,ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'newindex/newindex.html'
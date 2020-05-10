from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tag, Post, Category
from config.models import SideBar
from django.views.generic import DetailView, ListView
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
        # print(Category.get_navs())
        return context
#这里这个技巧真的是无语了。你看上面安格get_context_data方法，这个应该是类里的方法。但是这里没有继承任何类。
#但是！下面的类继承这个类，那这个get_context_data方法就是下面这个类里面的了，它会自动覆盖掉原本ListView的这个函数！
#这个技巧怕是我这样的脑子学不会的。
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'newindex/newindex.html'

class BlogIndexView(IndexView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/blogindex.html'

class postlistView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/blogpostlist.html'

class CategoryView(postlistView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category':category
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

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/blogdetails.html'
    pk_url_kwarg = 'post_id'

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
    template_name = 'aboutME/aboutme.html'

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
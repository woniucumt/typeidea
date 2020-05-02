from django.contrib import admin
from .models import Post, Category, Tag
from django.utils.html import format_html
from django.urls import reverse
from .adminforms import PostAdminForm
# Register your models here.
class PostInline(admin.TabularInline):#TabularInline不知道为何。
    fields = ('title', 'desc')
    extra = 1
    model = Post#d典型的我只知道这么配置，但是为啥我不知道，得看源码。

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ('name','status','is_nav','owner','created_time')
    fileds=('name','status','is_nav')
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = "文章数量"
    def __str__(self):
        return self.name
    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(CategoryAdmin,self).save_model(request,obj,form,change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields=('name','status')

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(TagAdmin,self).save_model(request,obj,form,change)

class CategoryOwnerFilter(admin.SimpleListFilter):
    #"自定义过滤器"
    title = '分类过滤器'
    parameter_name='owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.values())
        return queryset





@admin.register(Post )
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title','category','status',
        'created_time','owner','operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category__name']
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fields = (('category','title'),
              'desc','status','content','tag',)

    # fieldsets = (
    #     ('基础配置',{
    #         'description':'基础配置描述',
    #         'field':(
    #             ('title','category'),
    #             'status',
    #         ),
    #     }),
    # )


    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change',args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(PostAdmin,self).save_model(request,obj,form,change)
    def get_queryset(self,request):
        qs=super(PostAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)



from django.db import models
import mistune
# Create your models here.
from django.contrib.auth.models import User#其实不知道这一行是干什么的。user是写好的吗？怎么回事？
#注意根据ER图的。其实项目的开发真的很顺畅。
#咱们还是不要懒手敲一遍吧。
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    post_count = models.IntegerField(default=1,verbose_name = "文章数量")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        navs_count = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
                cate.post_count = Post.objects.filter(category=cate).count()
            else:
                normal_categories.append(cate)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
            'navs_count':navs_count
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'
        ordering = ['-id']

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    POST_ORIGNATE = "原创"
    POST_TRAMSMIT = "转载"
    POST_REPRINTE = "加工"
    IS_ORIGNAL = (
        (POST_ORIGNATE, '原创'),
        (POST_TRAMSMIT, '转载'),
        (POST_REPRINTE, '加工'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name="正文html代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_md = models.BooleanField(default=False, verbose_name="markdown语法")
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)#这个ondelete是几个意思。
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_orignal = models.CharField(max_length=255, default="原创", choices=IS_ORIGNAL, verbose_name="文章类型")
    is_topped = models.BooleanField(default=False, verbose_name="是否顶置")
    # 字数统计
    word_count = models.PositiveIntegerField(default=0,verbose_name="字数统计")
    read_time = models.PositiveIntegerField(default=12, verbose_name="建议阅读时间")

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    @classmethod
    def hot_post(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list = []
        else:
            post_list = tag.post_set.filter(status= Post.STATUS_NORMAL).select_related('owner','category')
        return post_list, tag
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list= []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')

        return post_list, category
    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def get_topped(cls):
        post_topped = cls.objects.filter(is_topped=True)
        return post_topped

    def save(self, *args, **kwargs):
        # self.content_html = mistune.markdown(self.content)
        self.content_html = self.content
        # self.word_count = len(self.content.split())
        super().save(*args, **kwargs)

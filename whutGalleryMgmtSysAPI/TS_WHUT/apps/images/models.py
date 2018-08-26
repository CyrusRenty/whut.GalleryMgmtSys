from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from easy_thumbnails.fields import ThumbnailerImageField
from DjangoUeditor.models import UEditorField

from my_utils.storage import ImageStorage

User = get_user_model()


class BannerModel(models.Model):
    # 轮播图
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", storage=ImageStorage(), verbose_name="轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name="访问地址")
    if_show = models.BooleanField(default=False, verbose_name="是否显示")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    desc = UEditorField(verbose_name="活动详情", imagePath="banner/images/", width=1000, height=300,
                        filePath="banner/files/", default='')

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ImageModel(models.Model):
    # 图片
    ACTIEVE_TYPE = (
        (1, "已通过"),
        (2, "等待审核"),
        (3, "未通过"),
    )

    image = ThumbnailerImageField(upload_to="images/%Y/%m", storage=ImageStorage(), blank=True,
                                  verbose_name="图片", max_length=100)
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    if_active = models.IntegerField(choices=ACTIEVE_TYPE, default=2, verbose_name="处理情况")
    desc = models.CharField(max_length=200, verbose_name="描述", null=True, blank=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, verbose_name="上传人")
    pattern = models.CharField(max_length=10, verbose_name="格式", default="jpeg")
    like_nums = models.IntegerField(default=0, verbose_name="点赞数")
    cates = models.CharField(max_length=200, verbose_name="层级划分", default="")
    collection_nums = models.IntegerField(default=0, verbose_name="收藏数")
    download_nums = models.IntegerField(default=0, verbose_name="下载量")
    name = models.CharField(max_length=20, verbose_name="图片名", default="")

    def url(self):
        from django.utils.safestring import mark_safe
        html = "<a href='/admin/users/userprofile/" + str(self.user.id) + "/update/'>" + self.user.username + "</>"
        if self.user.if_sign:
            html += "<i> 已签约</i>"
        if self.user.if_cer:
            html += "<i> 已认证</i>"
        return mark_safe(html)

    url.short_description = "上传者"

    def i_desc(self):
        if len(self.desc) > 5:
            return self.desc[:5] + '...'
        return self.desc

    i_desc.short_description = "图片描述"

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class Groups(models.Model):
    # 图片大类
    CATEGORY_TYPE = (
        (0, "三级类目"),
        (1, "二级类目"),
        (2, "一级类目"),
    )

    name = models.CharField(verbose_name="类别名称", max_length=20)
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    level = models.IntegerField(choices=CATEGORY_TYPE, default=1, verbose_name="层级")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属类目",
                               related_name="kids")
    if_show = models.BooleanField(default=False, verbose_name="是否展示")

    class Meta:
        verbose_name = "图片类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class SmallGroups(models.Model):
#     # 图片小类
#     name = models.CharField(verbose_name="小类名称", max_length=20)
#     add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
#     group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属大类",
#                               related_name="groups")
#
#     class Meta:
#         verbose_name = "图片小类"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name


class GroupImage(models.Model):
    # 小类与图片关联
    name = models.CharField(verbose_name="图片分类", max_length=20)
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    image = models.ForeignKey(ImageModel, models.CASCADE, verbose_name="图片")
    group = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="类别",
                              related_name="images")

    class Meta:
        verbose_name = "图片类别添加"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comment(models.Model):
    # 图片评论
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, verbose_name="图片")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="用户", related_name="speaker")
    reply = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="回复人", related_name="listen")
    content = models.CharField(max_length=200, verbose_name="评论")
    floor = models.IntegerField(verbose_name="楼数", default=0)
    is_add_info = models.BooleanField(verbose_name="是否回复", default=False)
    like = models.IntegerField(default=0, verbose_name="点赞数")
    num = models.IntegerField(default=0, verbose_name="投诉数量")

    class Meta:
        verbose_name = "图片评论"
        verbose_name_plural = verbose_name


class SearchWord(models.Model):
    # 被搜索词
    word = models.CharField(max_length=50, verbose_name="搜索词")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    num = models.IntegerField(default=1, verbose_name="搜索次数")

    class Meta:
        verbose_name = "被搜索词"
        verbose_name_plural = verbose_name

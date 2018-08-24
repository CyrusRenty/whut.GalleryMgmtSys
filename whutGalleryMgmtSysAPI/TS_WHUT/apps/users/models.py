from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

from my_utils.storage import ImageStorage


class UserProfile(AbstractUser):
    # 用户
    real_name = models.CharField(verbose_name="姓名", max_length=11, null=True, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=11, null=True, blank=True)
    p_class = models.CharField(verbose_name="专业班级", max_length=30, null=True, blank=True)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, blank=True, choices=(("male", "男"), ("female", "女")),
                              default="female", verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    number = models.CharField(max_length=20, verbose_name="学号", null=True, blank=True)
    image = models.ImageField(upload_to="heads/%Y/%m", default="heads/default.png", null=True, blank=True,
                              storage=ImageStorage(), max_length=100, verbose_name="头像")
    if_sign = models.BooleanField(verbose_name="签约", default=False)
    follow_nums = models.IntegerField(verbose_name="关注者量", default=0)
    fan_nums = models.IntegerField(verbose_name="粉丝量", default=0)
    upload_nums = models.IntegerField(verbose_name="上传量", default=0)
    like_nums = models.IntegerField(verbose_name="总点赞量", default=0)
    collection_nums = models.IntegerField(verbose_name="总收藏量", default=0)
    download_nums = models.IntegerField(verbose_name="总被下载量", default=0)
    desc = models.CharField(verbose_name="个人简介", max_length=150, blank=True)
    if_cer = models.BooleanField(verbose_name="是否认证", default=False)
    org_name = models.CharField(verbose_name="组织名字", default="", blank=True, max_length=50)
    id_card = models.ImageField(upload_to="id_cards/%Y/%m", null=True, blank=True, storage=ImageStorage(),
                                verbose_name="身份证图片")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    # 用户邮箱验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    send_email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"), ("update_email", "修改邮箱")),
                                 max_length=30, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "用户邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.send_email)


class Folder(models.Model):
    # 用户收藏夹
    name = models.CharField(max_length=20, verbose_name="收藏夹", default="默认文件夹")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")
    desc = models.CharField(max_length=150, verbose_name="描述", blank=True)
    nums = models.IntegerField(default=0, verbose_name="数量")
    update_time = models.DateField(default=datetime.now, verbose_name="更新时间")

    class Meta:
        verbose_name = '用户收藏夹'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserMessage(models.Model):
    # 用户消息
    post_user = models.CharField(max_length=20, default="图说理工网", verbose_name="发送用户")
    user = models.ForeignKey(UserProfile, models.CASCADE, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class Org(models.Model):
    # 组织
    image = models.ImageField(upload_to="org/%Y/%m", null=True, blank=True, storage=ImageStorage(),
                              verbose_name="认证图片")
    teacher = models.CharField(max_length=20, verbose_name="指导老师")
    name = models.CharField(max_length=50, verbose_name="组织名称")
    user = models.ForeignKey(UserProfile, models.CASCADE, verbose_name="关联用户")
    status = models.CharField(max_length=5, default="1", verbose_name="认证状态",
                              choices=(("1", "等待认证"),
                                       ("2", "通过认证"),
                                       ("3", "未通过认证")))
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "组织认证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

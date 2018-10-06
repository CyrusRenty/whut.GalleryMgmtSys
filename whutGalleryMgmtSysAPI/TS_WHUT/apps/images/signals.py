import imghdr
import re
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import ImageModel, GroupImage, Groups
from my_utils.add_wa import add_wa


@receiver(pre_delete, sender=ImageModel)
def delete_image_num(sender, instance=None, **kwargs):
    """
    当删除一张图片时
    """
    # 减少上传数目
    user = instance.user
    user.upload_nums -= 1
    user.save()


@receiver(pre_save, sender=ImageModel)
def do_something_if_changed(sender, instance, **kwargs):
    """
    在图片保存之前, 需要检查图片的类别是否是已存在的类别
    不是的话回退类别
    """
    try:
        obj = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        # 图片才被创建
        pass
    else:
        if obj.cates != instance.cates:
            if '/' in obj.cates or '、' in obj.cates:
                cates = re.split('[/、]', obj.cates)
                for cate in cates:
                    group = Groups.objects.filter(name=cate)
                    if not group.count() or group[0].level == 2:
                        # 回退
                        obj.cates = instance.cates
                        break


@receiver(post_save, sender=ImageModel)
def create_group_image(sender, instance=None, created=False, **kwargs):
    """
    当上传图片动作发生
    """
    if created:
        # 增加上传数目
        user = instance.user
        user.upload_nums += 1
        user.save()
        # 保存图片格式
        pattern = imghdr.what(instance.image.path)
        instance.pattern = pattern
        # 保存图片种类
        cates = instance.cates.split(" ")
        cate_str = ''
        for cate in cates:
            if cate:
                group = Groups.objects.filter(name=cate)
                if group.count():

                    group = group[0]
                    GroupImage(image=instance, name=cate, group=group).save()

                    tmp_str = group.name

                    while group.parent:
                        tmp_str = group.parent.name + '/' + tmp_str
                        group = group.parent

                    cate_str = cate_str + '、' + tmp_str
                else:
                    cate_str = cate_str + '、' + cate
                    # 没有该分类也不创建该分类
                    # group = Groups(name=cate)
                    # group.save()
                    # GroupImage(image=instance, name=cate, group=group).save()

        instance.cates = cate_str[1:]
        instance.save()

        # 生成水印图
        path = instance.image.path
        name = path.rsplit('/', 1)[1]
        add_wa(path, name)

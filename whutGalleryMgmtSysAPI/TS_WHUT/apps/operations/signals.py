from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from datetime import datetime
from .models import LikeShip, DownloadShip, Follow, UserFolderImage, CommentLike, Application, Report


@receiver(post_save, sender=Report)
def create_report(sender, instance=None, created=False, **kwargs):
    """
    当举报评论时和举报状态改变时 
    """
    # 评论举报数量+1
    if created:
        comment = instance.comment
        comment.num += 1
        comment.save()
    # 举报通过, 评论删除
    elif instance.status == '2':
        comment = instance.comment
        comment.delete()


@receiver(post_save, sender=Application)
def change_if_sign(sender, instance=None, created=False, **kwargs):
    """
    当签约动作完成
    """
    if instance.status == '3':
        # 用户状态改成已签约, 结束等待
        user = instance.user
        user.if_sign = True
        user.save()
    else:
        user = instance.user
        user.if_sign = False
        user.save()


@receiver(post_save, sender=CommentLike)
def create_comment_like_num(sender, instance=None, created=False, **kwargs):
    """
    当点赞评论动作发生
    """
    if created:
        # 评论点赞数加1
        comment = instance.comment
        comment.like += 1
        comment.save()


@receiver(pre_delete, sender=CommentLike)
def delete_comment_like_num(sender, instance=None, **kwargs):
    """
    当取消点赞评论动作发生
    """
    # 评论点赞数减1
    comment = instance.comment
    comment.like -= 1
    comment.save()


@receiver(post_save, sender=UserFolderImage)
def create_collect_num(sender, instance=None, created=False, **kwargs):
    """
    当收藏图片动作发生
    """
    if created:
        # 图片收藏数加1
        image = instance.image
        image.collection_nums += 1
        image.save()
        # 图片上传者总收藏数加1
        user = image.user
        user.collection_nums += 1
        user.save()
        # 收藏夹图片数量加1,更新时间变化
        folder = instance.folder
        folder.nums += 1
        folder.update_time = datetime.now()
        folder.save()


@receiver(pre_delete, sender=UserFolderImage)
def delete_collect_num(sender, instance=None, **kwargs):
    """
    当取消收藏图片动作发生 
    """
    # 图片收藏数减1
    image = instance.image
    image.collection_nums -= 1
    image.save()
    # 图片上传者总收藏数减1
    user = image.user
    user.collection_nums -= 1
    user.save()
    # 收藏夹图片数量减1,更新时间变化
    folder = instance.folder
    folder.nums -= 1
    folder.update_time = datetime.now()
    folder.save()


@receiver(post_save, sender=Follow)
def create_follow_num(sender, instance=None, created=False, **kwargs):
    """
    当关注动作发生 
    """
    if created:
        # 粉丝的关注者数量加1
        fan = instance.fan
        fan.follow_nums += 1
        fan.save()
        # 被关注着的粉丝数量加1
        follow = instance.follow
        follow.fan_nums += 1
        follow.save()


@receiver(pre_delete, sender=Follow)
def delete_follow_num(sender, instance=None, **kwargs):
    """
    当取消关注动作发生
    """
    # 粉丝的关注者数量减1
    fan = instance.fan
    fan.follow_nums -= 1
    fan.save()
    # 被关注着的粉丝数量减1
    follow = instance.follow
    follow.fan_nums -= 1
    follow.save()


@receiver(post_save, sender=LikeShip)
def create_like_num(sender, instance=None, created=False, **kwargs):
    """
    当点赞图片动作发生
    """
    if created:
        # 图片点赞量加1
        image = instance.image
        image.like_nums += 1
        image.save()
        # 用户总图片点赞量加1
        user = image.user
        user.like_nums += 1
        user.save()


@receiver(pre_delete, sender=LikeShip)
def delete_like_num(sender, instance=None, **kwargs):
    """
    当取消点赞图片动作发生 
    """
    # 图片点赞量减1
    image = instance.image
    image.like_nums -= 1
    image.save()
    # 用户总图片点赞量减1
    user = image.user
    user.like_nums -= 1
    user.save()


@receiver(post_save, sender=DownloadShip)
def create_download_num(sender, instance=None, created=False, **kwargs):
    """
    当下载图片动作发生
    """
    if created:
        # 图片下载量加1
        image = instance.image
        image.download_nums += 1
        image.save()
        # 用户总图片下载量加1
        user = image.user
        user.download_nums += 1
        user.save()

import django_filters

from .models import ImageModel, Comment


class ImageFilter(django_filters.rest_framework.FilterSet):
    """
    图片的过滤类
    """
    class Meta:
        model = ImageModel
        fields = ['pattern', 'user']


class CommentFilter(django_filters.rest_framework.FilterSet):
    """
    评论过滤类
    """
    class Meta:
        model = Comment
        fields = ['image']

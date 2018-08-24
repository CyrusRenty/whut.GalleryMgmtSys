from django.db.models import Q
from rest_framework import status
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework_extensions.cache.mixins import CacheResponseMixin  # 缓存
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle  # 限速
import jieba

from .models import ImageModel, BannerModel, Comment, SearchWord, Groups, SmallGroups, GroupImage
from .serializer import (ImageSerializer, ImageCreateSerializer, BannerSerializer, CommentListSerializer,
                         CommentCreateSerializer, BannerOneSerializer, SearchWordSerializer, GroupListSerializer)
from .filters import ImageFilter, CommentFilter


class ImagePagination(PageNumberPagination):
    """
    图片分页
    page_size: 每页大小
    page_size_query_param: 每页大小参数名
    page_query_param: 第几页参数名
    max_page_size: 最大页数
    """
    page_size = 8
    page_size_query_param = 'num'
    page_query_param = "page"


class GroupsViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        全部大类加上大类中全部小类图片
    retrieve:
        获取全部大类的图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = GroupListSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('add_time', 'like_nums', 'collection_nums')
    queryset = Groups.objects.filter(if_show=True)

    @property
    def pagination_class(self):
        if self.action == 'list':
            return None
        return ImagePagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        groups = SmallGroups.objects.filter(group=instance)

        q = Q()
        q.connector = 'OR'

        for group in groups:
            q.children.append(('group', group))

        small_groups = GroupImage.objects.filter(q)
        images = ImageModel.objects.filter(groupimage__in=small_groups, if_active=True)

        queryset = self.filter_queryset(images)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupListSerializer
        return ImageSerializer


class SmallGroupsViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        获取某个小类别全部图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ImageSerializer
    queryset = SmallGroups.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('add_time', 'like_nums', 'collection_nums')
    pagination_class = ImagePagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        groups = GroupImage.objects.filter(group=instance)
        images = ImageModel.objects.filter(groupimage__in=groups, if_active=True)

        queryset = self.filter_queryset(images)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)


class ImageViewset(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
        显示所有图片,时间倒序
    create:
        上传一张图片
    retrieve:
        显示一张图片
    destroy:
        删除一张图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = ImageFilter
    ordering_fields = ('add_time', 'like_nums', 'collection_nums')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'retrieve'):
            return [permissions.IsAuthenticated()]
        return []

    def get_queryset(self):
        # 删除只能是上传者
        if self.action == 'destroy':
            return ImageModel.objects.filter(user=self.request.user)
        return ImageModel.objects.filter(if_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageSerializer
        elif self.action == 'create':
            return ImageCreateSerializer
        return ImageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        search = request.GET.get('search')

        if queryset.count():
            # 搜索使用两种方式, 一种是有逗号区分, 每个逗号切分的词就是关键词.
            # 这一部分是为了给前端中分类做的.
            # 另外一种就是利用分词来检索, 这一部分是为了给检索做的.
            # 检索一共搜cates字段, name字段, desc字段, user.username字段.
            if search:

                # 搜索词数目加1, 或者创建搜索词
                words = SearchWord.objects.filter(word=search)
                if words.count():
                    words[0].num += 1
                else:
                    SearchWord(word=search).save()

                rows = ('cates', 'name', 'desc', 'user__username')
                q = Q()
                q.connector = 'OR'
                for row in rows:
                    if ',' in search:
                        kws = search.replace(',', ' ').split()
                        for kw in kws:
                            q.children.append((row+'__icontains', kw))
                    else:
                        kws = jieba.cut_for_search(search)
                        for kw in kws:
                            q.children.append((row+'__icontains', kw))
                queryset = queryset.filter(q)

            page = self.paginate_queryset(queryset[::-1])

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SearchWordViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取热搜词
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = BannerModel.objects.all().order_by("-num")[:10]
    serializer_class = SearchWordSerializer


class BannerViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = BannerModel.objects.filter(if_show=True)
    serializer_class = BannerSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BannerOneSerializer
        return BannerSerializer


class CommentPagination(PageNumberPagination):
    """
    评论分页
    """
    page_size = 8
    page_size_query_param = 'num'
    page_query_param = "page"


class CommentViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        列出单张图片的全部评论
    create:
        添加评论
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Comment.objects.filter(is_add_info=False).order_by("-floor")
    pagination_class = CommentPagination
    serializer_class = CommentListSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CommentFilter
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentCreateSerializer

    def get_reply(self, image, start, end):
        queryset = Comment.objects.filter(is_add_info=True, image_id=image, floor__gte=start, floor__lte=end).order_by("floor")
        return self.get_serializer(queryset, many=True).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        data = serializer.data
        data['user'] = {'id': obj.user.id, 'username': obj.user.username, 'image': obj.user.image.url}
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 因为是倒序排的
            start = serializer.data[-1]['floor']
            end = serializer.data[0]['floor']

            replys = self.get_reply(int(request.GET.get('image')), start, end)
            data = serializer.data
            replys_len = len(replys)

            for one in data:
                i = 0
                while i < replys_len and one['floor'] >= replys[i]['floor']:
                    if one['floor'] == replys[i]['floor']:
                        one.setdefault('kids', []).append(replys[i])
                    i += 1

            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

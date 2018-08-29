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
import datetime
from django.db.models import Count

from .models import ImageModel, BannerModel, Comment, SearchWord, Groups, GroupImage
from operations.models import DownloadShip, UserFolderImage, LikeShip, Follow
from .serializer import (ImageSerializer, ImageCreateSerializer, BannerSerializer, CommentListSerializer,
                         CommentCreateSerializer, BannerOneSerializer, SearchWordSerializer, GroupListSerializer,
                         ImageUpdateSerializer)
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


def check_cates(instance):
    """
    这里迭代查询一个类别的里层类别
    :param instance: Group对象
    :return: tuple
    """
    i = instance.level
    if i > 1:
        instance = Groups.objects.filter(parent=instance)
        i -= 1
        while i > 1:
            instance = Groups.objects.filter(parent__in=instance)
            i -= 1
        # 如果涉及到增加第三层
        q2 = Groups.objects.filter(parent__in=instance)
    else:
        # 如果涉及到增加第三层
        q2 = Groups.objects.filter(parent=instance)

    return instance, q2


class GroupsViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        全部大类加上大类中全部小类图片
    retrieve:
        获取全部大类的图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = GroupListSerializer
    ordering_fields = ('add_time', 'like_nums', 'collection_nums')

    def get_queryset(self):
        if self.action == 'list':
            return Groups.objects.filter(if_show=True, level=2)
        return Groups.objects.filter(if_show=True)

    @property
    def filter_backends(self):
        if self.action == 'list':
            return []
        return [filters.OrderingFilter]

    @property
    def pagination_class(self):
        if self.action == 'list':
            return None
        return ImagePagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.if_show:
            return Response({"error": "该层不显示"}, status=400)

        q, q2 = check_cates(instance)

        # 如果涉及到增加第三层
        if q2.count():
            if isinstance(q, Groups):
                ship = GroupImage.objects.filter(Q(group=q) | Q(group__in=q2))
            else:
                ship = GroupImage.objects.filter(Q(group__in=q) | Q(group__in=q2))
        elif isinstance(q, Groups):
            ship = GroupImage.objects.filter(group=q)
        else:
            ship = GroupImage.objects.filter(group__in=q)

        images = ImageModel.objects.filter(groupimage__in=ship, if_active=1)

        # 格式筛选,用户名筛选
        pattern = request.GET.get('pattern')
        user = request.GET.get('user')
        if pattern:
            images = images.filter(pattern=pattern)
        if user:
            images = images.filter(user_id=int(user))

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


def filter_cate(cates, images):
    """根据分类筛选图片,例如url末尾是?cates=人物,生活,菁菁校园
    :param cates: cates
    :param images: queryset
    :return: queryset
    """
    cates = cates.split(',')
    queryset = images.filter(groupimage__name=cates[0])
    if not queryset.count():
        groups = Groups.objects.filter(name=cates[0])
        if groups.count():
            groups = Groups.objects.filter(parent=groups[0])
            queryset = images.filter(groupimage__group__in=groups)

    if len(cates) > 1:
        for cate in cates[1:]:
            queryseted = queryset.filter(groupimage__name=cate)
            nums = queryseted.count()

            # 如果是第一层类别
            if nums == 0:
                groups = Groups.objects.filter(name=cate)
                if groups.count():
                    groups = Groups.objects.filter(parent=groups[0])
                    queryset = queryset.filter(groupimage__group__in=groups)
            else:
                queryset = queryseted

    return queryset


def save_hot_word(search_word):
    """
    保存搜索词 利用分词来检索
    检索一共搜cates字段, name字段, desc字段, user.username字段.
    :param search_word: 搜索词
    :return: Q的对象
    """
    words = SearchWord.objects.filter(word=search_word)
    if words.count():
        words[0].num += 1
    else:
        SearchWord(word=search_word).save()

    rows = ('cates', 'name', 'desc', 'user__username')
    q = Q()
    q.connector = 'OR'
    for row in rows:
        kws = jieba.cut_for_search(search_word)
        for kw in kws:
            q.children.append((row + '__icontains', kw))
    return q


def get_upload_nums(user):
    return ImageModel.objects.filter(user=user, if_active=1).count()


def get_if_like(request, image):
    if not request.user.is_authenticated:
        return False
    ship = LikeShip.objects.filter(user_id=request.user.id, image_id=image.id)
    if ship.count():
        return ship[0].id
    return False


def get_user_data(image):
    user = image.user
    return {
        "image": user.image.url,
        "id": user.id,
        "username": user.username,
        "upload_nums": get_upload_nums(user),
        "fan_nums": user.fan_nums
    }


def get_if_follow(request, image):
    # 是否关注上传者
    if not request.user.is_authenticated:
        return False
    ship = Follow.objects.filter(fan_id=request.user.id, follow_id=image.user.id)
    if ship.count():
        return ship[0].id
    return False


def get_if_collect(request, image):
    if not request.user.is_authenticated:
        return False
    ship = UserFolderImage.objects.filter(user_id=request.user.id, image_id=image.id)
    if ship.count():
        return ship[0].id
    return False


class ImageViewset(viewsets.ModelViewSet):
    """
    list:
        显示所有图片,时间倒序
    create:
        上传一张图片
    retrieve:
        显示一张图片
    destroy:
        删除一张图片
    update:
        修改一张图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ImageSerializer
    pagination_class = ImagePagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = ImageFilter
    ordering_fields = ('add_time', 'like_nums', 'collection_nums', 'download_nums')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ('create', 'destroy', 'update'):
            return [permissions.IsAuthenticated()]
        return []

    def get_queryset(self):
        # 删除只能是上传者
        if self.action == 'destroy':
            return ImageModel.objects.filter(user=self.request.user)
        if self.action == 'update':
            return ImageModel.objects.filter(user=self.request.user, if_active=4)
        return ImageModel.objects.filter(if_active=1)

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageSerializer
        elif self.action == 'create':
            return ImageCreateSerializer
        elif self.action == 'update':
            return ImageUpdateSerializer
        return ImageSerializer

    def get_serializer_context(self):
        """
        重载, 目的是只有retrieve接口才会显示水印图, 其他应该是缩略图
        专为/images/的retrieve接口设置一个信号,因为使用ImageSerializer的比较多
        """
        if self.action == 'retrieve':
            return {
                'request': self.request,
                'format': self.format_kwarg,
                'view': self,
                'water_image': True
            }
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def page_serializer(self, qs, page, request, Klass):
        """
        分页和序列化, 不能直接用id筛选再序列化, 因为有一个图片顺序, 所以只有自己序列化了
        """
        sum_qs = qs.count()
        if (page - 1) * 8 > sum_qs:
            return Response([])
        if page * 8 < sum_qs:
            qs = qs[(page - 1) * 8:page * 8]
            next_page = page + 1
        else:
            qs = qs[(page - 1) * 8:]
            next_page = None

        # 序列化
        results = []
        for q in qs:
            image = ImageModel.objects.get(id=q['image'])
            if isinstance(Klass, DownloadShip):
                download_nums = q['total_image']
                collection_nums = image.collection_nums
            else:
                download_nums = image.download_nums
                collection_nums = q['total_image']
            results.append({
                "id": image.id,
                "name": image.name,
                "cates": image.cates,
                "like_nums": image.like_nums,
                "collection_nums": collection_nums,
                "download_nums": download_nums,
                "user": get_user_data(image),
                "image": image.image['avatar'].url,
                "if_like": get_if_like(request, image),
                "if_follow": get_if_follow(request, image),
                "if_collect": get_if_collect(request, image)
            })

        return Response({
            "count": sum_qs,
            "next": next_page,
            "results": results
        })

    def rank(self, kw, time, request):
        """周,月排行榜"""
        # 处理下载还是收藏
        Klass = UserFolderImage
        if kw == '-download_nums':
            Klass = DownloadShip

        # 处理周或者月
        now_time = datetime.datetime.now()
        if time == 'week':
            day_num = now_time.isoweekday()
            monday = (now_time - datetime.timedelta(days=day_num))
            time_range = (monday, now_time)
        elif time == 'month':
            month = now_time.month
            if month == 12:
                month = 0
            last_day = datetime.datetime(now_time.year, month + 1, 1, 0, 0, 0)
            first_day = datetime.datetime(now_time.year, now_time.month, 1, 0, 0, 0)
            time_range = (first_day, last_day)
        else:
            return Response({"time": "参数错误"}, status=400)

        # 查询排行情况
        qs = Klass.objects.filter(add_time__range=time_range).values('image').annotate(
            total_image=Count("image")).order_by("-total_image")

        # 分页
        page = request.GET.get('page')
        page = 1 if not page else int(page)
        return self.page_serializer(qs, page, request, Klass)

    def list(self, request, *args, **kwargs):
        if_active = request.GET.get('if_active')
        user = request.GET.get('user')
        # 获得用户上传图片,在草稿箱或等待上传或通过审核或没通过
        if if_active:
            if user and int(user) == request.user.id:
                queryset = self.filter_queryset(self.get_queryset())
            else:
                return Response({"error": "没有权限"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            queryset = ImageModel.objects.filter(if_active=1)
            # 检索
            search = request.GET.get('search')
            if search:
                queryset = queryset.filter(save_hot_word(search))
            # 筛选分类
            cates = request.GET.get('cates')
            if cates:
                queryset = filter_cate(cates, queryset)
            # 排序加周榜和月榜
            kw = request.GET.get('ordering')
            time = request.GET.get('time')
            if kw in ('-download_nums', '-collection_nums') and time:
                return self.rank(kw, time, request)
            queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SearchWordViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取热搜词
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = SearchWord.objects.all().order_by("-num")[:10]
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

from rest_framework import viewsets
from django.views.generic.base import View
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Count
import json
import datetime
from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .serializer import (FolderCreateSerializer, FolderListSerializer, FolderOneSerializer, FolderUpdateSerializer,
                         UserListSerializer, UserCreateSerializer, UserUpdateSerializer, OrgSerializer, OrgOneSerializer)
from .models import Folder, UserMessage, Org
from images.models import ImageModel
from operations.models import DownloadShip, UserFolderImage, Follow
from my_utils.send_email import send_register_email
from .filters import UsersFilter

User = get_user_model()


class ResetEmail(View):
    def post(self, request):
        email = request.POST.get('email')
        if not email:
            return HttpResponse(json.dumps({"error": "参数错误"}), content_type="application/json")
        user_message = UserMessage()
        user_message.user = request.user
        user_message.message = "图说理工网修改邮箱"
        user_message.save()
        send_register_email(email, "update_email")
        pass


class HasUser(View):
    def get(self, request):
        username = request.GET.get('username')
        email = request.GET.get('email')
        if username:
            users = User.objects.filter(username=username)
            if users.count():
                if not users[0].is_active:
                    return HttpResponse(json.dumps({"msg": True, "status": True}), content_type="application/json")
                return HttpResponse(json.dumps({"msg": True}), content_type="application/json")
        elif email:
            users = User.objects.filter(email=email)
            if users.count():
                if not users[0].is_active:
                    return HttpResponse(json.dumps({"msg": True, "status": True}), content_type="application/json")
                return HttpResponse(json.dumps({"msg": True}), content_type="application/json")
        return HttpResponse(json.dumps({"msg": False}), content_type="application/json")


class OrgViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        得到个人认证状态
    create:
        新建认证
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrgSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            serializer.data[0]['status'] = int(serializer.data[0]['status'])
            return Response(serializer.data[0])
        return Response({'status': 0})

    def get_serializer_class(self):
        if self.action == 'list':
            return OrgOneSerializer
        return OrgSerializer

    def get_queryset(self):
        return Org.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = self.perform_create(serializer)
        org.user = request.user
        org.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class FolderViewset(viewsets.ModelViewSet):
    """
    list:
        获取用户全部收藏夹
    create:
        创建一个收藏夹
    retrieve:
        获取一个收藏夹的全部图片
    update:
        修改收藏夹名字
    destroy:
        删除一个收藏夹
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 只能对自己的收藏夹操作
        return Folder.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FolderCreateSerializer
        elif self.action == 'list':
            return FolderListSerializer
        elif self.action == 'retrieve':
            return FolderOneSerializer
        return FolderUpdateSerializer


class UserPagination(PageNumberPagination):
    """
    用户分页
    page_size: 每页大小
    page_size_query_param: 每页大小参数名
    page_query_param: 第几页参数名
    max_page_size: 最大页数
    """
    page_size = 8
    page_size_query_param = 'num'
    page_query_param = "page"
    max_page_size = 100


class UserViewset(viewsets.ModelViewSet):
    """
    list:
        获取全部用户, (按下载量,收藏量,关注量排序)
    create:
        注册用户
    retrieve:
        获取用户信息
    update:
        修改用户信息
    destroy:
        删除用户
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = UserListSerializer
    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = UsersFilter
    ordering_fields = ('fan_nums', 'download_nums', 'collection_nums')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_image(self, user, request):
        """获取用户三张图片"""
        data = []
        i = 0
        for image in ImageModel.objects.filter(user=user, if_active=1)[::-1]:
            i += 1
            if i > 3:
                return data
            data.append({
                "url": image.image['avatar'].url,
                "id": image.id,
            })
        return data

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
        qs = Klass.objects.filter(add_time__range=time_range).values('image__user').annotate(
            total_user=Count("image__user")).order_by("-total_user")

        # 分页
        page = request.GET.get('page')
        page = 1 if not page else int(page)
        sum_qs = qs.count()
        if (page-1)*8 > sum_qs:
            return Response([])
        if page*8 < sum_qs:
            qs = qs[(page-1)*8:page*8]
            next_page = page+1
        else:
            qs = qs[(page-1)*8:]
            next_page = None

        # 序列化
        results = []
        for q in qs:
            user = User.objects.get(id=q['image__user'])
            ship = Follow.objects.filter(fan_id=request.user.id, follow_id=user.id)
            if ship.count():
                if_follow = ship[0].id
            else:
                if_follow = False
            results.append({
                "id": user.id,
                "fan_nums": user.fan_nums,
                "username": user.username,
                "if_cer": user.if_cer,
                "if_sign": user.if_sign,
                "if_follow": if_follow,
                "images": self.get_image(user, request)
            })

        return Response({
            "count": sum_qs,
            "next": next_page,
            "results": results
        })

    def list(self, request, *args, **kwargs):
        kw = request.GET.get('ordering')
        time = request.GET.get('time')
        if kw in ('-download_nums', '-collection_nums') and time:
            return self.rank(kw, time, request)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'destroy':
            return User.objects.filter(id=self.request.user.id)
        elif self.action == 'update':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ("create", "retrieve", "list"):
            return []
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        pwd = make_password(user.password)
        user.password = pwd
        user.is_active = False
        user.save()
        headers = self.get_success_headers(serializer.data)

        # 写入欢迎注册消息
        user_message = UserMessage()
        user_message.user = user
        user_message.message = "欢迎注册图说理工网"
        user_message.save()

        # 发送验证邮箱
        send_register_email(user.email, "register")

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = self.perform_update(serializer)

        if not user.is_active:
            user_message = UserMessage()
            user_message.user = user
            user_message.message = "图说理工网-验证个人信息修改"
            user_message.save()
            # 发送验证邮箱
            send_register_email(user.email, "register")

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

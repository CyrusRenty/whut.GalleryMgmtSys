from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import View
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.pagination import PageNumberPagination
import json
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle  # 限速

from .serializer import (LikeSerializer, FollowSerializer, CollectSerializer, DownloadSerializer, CommentLikeSerialzer,
                         LikeListSerializer, DownloadListSerializer, FollowListSerializer, FanListSerializer,
                         ApplicationListSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer,
                         ReportSerializer)
from .models import LikeShip, Follow, UserFolderImage, DownloadShip, CommentLike, Application
from users.models import EmailVerifyRecord, UserMessage
from images.models import ImageModel
from my_utils.send_email import send_register_email

User = get_user_model()


class ReportViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        举报评论
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportSerializer


class FollowUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部关注用户
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FollowListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(fan=self.request.user)


class FanUserViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全部粉丝
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FanListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(follow=self.request.user)


class CollectViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加图片到收藏夹
    destroy:
        从收藏夹删除图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = CollectSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # 删除只能是该用户收藏
        return UserFolderImage.objects.filter(user=self.request.user)


class LikeViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户点赞图片
    create:
        点赞一张图片
    destroy:
        取消点赞一张图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = LikeSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return LikeListSerializer
        return LikeSerializer

    def get_queryset(self):
        # 删除只能是点赞者
        return LikeShip.objects.filter(user=self.request.user)


class FollowViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        关注用户
    destroy:
        取消关注
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = FollowSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return FollowSerializer

    def get_queryset(self):
        # 取消只能是关注者
        return Follow.objects.filter(fan=self.request.user)


class DownloadPagination(PageNumberPagination):
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
    max_page_size = 100


class DownloadViewset(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    create:
        下载图片
    list:
        获取用户下载图片
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = DownloadSerializer
    pagination_class = DownloadPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return DownloadShip.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return DownloadListSerializer
        return DownloadSerializer

    def create(self, request, *args, **kwargs):
        # 下载图片返回原图url
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ship = self.perform_create(serializer)

        re_dict = serializer.data
        re_dict['url'] = 'http://' + self.request._request.META['HTTP_HOST'] + ship.image.image.url

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class CommentLikeViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加点赞评论
    destroy:
        取消点赞评论
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = CommentLikeSerialzer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CommentLike.objects.filter(user=self.request.user)


class ApplicationViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取个人签约状态
    create:
        添加签约申请
    update:
        修改申请状态
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    serializer_class = ApplicationListSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

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
        return Response({"status": 0})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.status != '1':
            return Response({"error": "没有同意合约"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        serializer.data['status'] = int(serializer.data['status'])
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ship = self.perform_create(serializer)
        ship.status = '1'
        ship.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        elif self.action == 'create':
            return ApplicationCreateSerializer
        return ApplicationUpdateSerializer

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)


class ActiveUserView(View):
    """
    注册用户激活
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                # 得到一个用户信息邮箱与传来的邮箱验证邮箱相同的用户信息实例
                user = User.objects.get(email=record.send_email)
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    record.delete()
                    return HttpResponseRedirect('/tslg/')
        return render(request, "active_fail.html", {"error": "激活失败: 激活链接失效!"})


class ForgetView(View):
    def post(self, request):
        """
        点击忘记密码后前端会有一个忘记密码的界面,
        然后用户会填写邮箱,
        给用户发送验证邮箱, 等待用户确认邮箱
        """
        email = request.POST.get("email")
        if not email:
            return HttpResponse(json.dumps({"error": "参数错误"}), content_type="application/json")
        users = User.objects.filter(email=email)
        if not users.count():
            return HttpResponse(json.dumps({"error": "邮箱错误"}), content_type="application/json")
        user = users[0]
        # 保存用户信息
        user_message = UserMessage()
        user_message.user = user
        user_message.message = "图说理工网修改密码"
        user_message.save()
        # 发送邮件
        send_register_email(email, "forget")
        return HttpResponse(json.dumps({"msg": "请前往邮箱验证"}), content_type="application/json")


class ResetPwdView(View):
    def get(self, request, active_code):
        """
        从忘记密码的验证邮箱点击进入这里,
        用户不用输入用户名或邮箱, 这里直接得到用户的信息,
        界面里用户可以直接输入新密码
        """
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records.count():
            for record in all_records:
                email = record.send_email
                user = User.objects.get(email=email)
                record.delete()
                return render(request, "password_reset.html", {"id": str(user.id)})

        # return render(request, "password_reset.html", {"id": 1})
        # 邮箱填写错误, 不能修改密码
        return render(request, "active_fail.html", {"error": "邮箱错误: 没有该邮箱用户!"})


class ChangePasswordView(View):
    def post(self, request):
        """
        由修改密码的面发送POST请求过来
        返回json判断是否修改成功
        """
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        user_id = request.POST.get("id")
        if not user_id:
            return render(request, "active_fail.html", {"error": "验证错误: 页面已失效!"})
        user = User.objects.filter(id=int(user_id))[0]
        if len(password1) < 6:
            return render(request, "password_reset.html", {"id": str(user.id), "error": "密码长度最少6位!"})
        if password1 != password2:
            return render(request, "password_reset.html", {"id": str(user.id), "error": "密码不一致!"})
        user.password = make_password(password1)
        user.save()
        return render(request, "password_reset.html", {"msg": "修改成功!"})


class UserImageView(View):
    def get(self, request, user_id):
        """
        用户签约审查界面的跳转
        """
        if request.user.is_authenticated and request.user.is_staff:
            images = ImageModel.objects.filter(user_id=user_id, if_active=True)
            target_user = User.objects.get(id=user_id)
            return render(request, 'images.html', {
                "user": target_user,
                "images": images,
            })


class CheckView(View):
    def post(self, request):
        """
        提交审查的结果, 结果为通过或者不通过
        """
        res = request.POST.get('radio')
        user_id = request.POST.get('user')
        ship = Application.objects.get(user_id=int(user_id))
        if res:
            if res == 'n':
                ship.status = 4
            elif res == 'y':
                ship.status = 3
            ship.save()
            # 很奇怪, 信号量没有起作用, 所以在这里直接改
            user = ship.user
            user.if_sign = True
            user.save()
            return HttpResponseRedirect('/admin/')

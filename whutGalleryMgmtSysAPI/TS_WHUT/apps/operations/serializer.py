from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import LikeShip, DownloadShip, Follow, UserFolderImage, CommentLike, Application, Report
from images.serializer import ImageSerializer
from images.serializer import UserBrifSerializer


class ReportSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['user'] != self.context['request'].user:
            raise serializers.ValidationError('没有权限')
        return attrs

    class Meta:
        model = Report
        fields = ('user', 'comment', 'content', 'reason')


class CollectSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['user'] != self.context['request'].user or not attrs['image'].if_active:
            raise serializers.ValidationError('没有权限')
        return attrs

    class Meta:
        model = UserFolderImage
        fields = ('folder', 'image', 'id', 'user')

    validators = [
        UniqueTogetherValidator(
            queryset=UserFolderImage.objects.all(),
            fields=('user', 'image', 'folder'),
            message="已经收藏"
        )
    ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeShip
        fields = ('user', 'image', 'id')

    def validate(self, attrs):
        if attrs['user'] != self.context['request'].user or not attrs['image'].if_active:
            raise serializers.ValidationError('没有权限')
        return attrs

    validators = [
        UniqueTogetherValidator(
            queryset=LikeShip.objects.all(),
            fields=('user', 'image'),
            message="已经点赞"
        )
    ]


class LikeListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = LikeShip
        fields = ('user', 'image', 'id')


class DownloadSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not attrs['image'].if_active:
            raise serializers.ValidationError('没有权限')
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = DownloadShip
        fields = ('image',)


class DownloadListSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = DownloadShip
        fields = ('user', 'image', 'id', 'add_time')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follow', 'fan', 'id')

    def validate(self, attrs):
        if attrs['follow'] == attrs['fan']:
            raise serializers.ValidationError('不能关注自己')
        if attrs['fan'] != self.context['request'].user:
            raise serializers.ValidationError('没有权限')
        return attrs

    validators = [
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('follow', 'fan'),
            message="已经关注"
        )
    ]


class FollowListSerializer(serializers.ModelSerializer):
    follow = UserBrifSerializer()

    class Meta:
        model = Follow
        fields = ('follow', 'id')


class FanListSerializer(serializers.ModelSerializer):
    fan = UserBrifSerializer()

    class Meta:
        model = Follow
        fields = ('fan', 'id')


class CommentLikeSerialzer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs.get('user'):
            return attrs
        raise serializers.ValidationError('参数错误')

    class Meta:
        model = CommentLike
        fields = ('user', 'comment', 'id')

    validators = [
        UniqueTogetherValidator(
            queryset=CommentLike.objects.all(),
            fields=('user', 'comment'),
            message="已经点赞"
        )
    ]


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('user', 'status', 'id')


class ApplicationCreateSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=Application.objects.all(),
            fields=('user',),
            message="已经申请"
        )
    ]

    class Meta:
        model = Application
        fields = ('user', 'id')


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        name = self.initial_data.get('name')
        p_class = self.initial_data.get('p_class')
        mobile = self.initial_data.get('mobile')
        qq = self.initial_data.get('qq')
        id_card = self.initial_data.get('id_card')
        user = self.context['request'].user
        if not (name and p_class and mobile and qq and id_card):
            raise serializers.ValidationError('参数错误')
        user.real_name = name
        user.p_class = p_class
        user.mobile = mobile
        user.qq = qq
        user.id_card = id_card
        user.save()
        return attrs

    class Meta:
        model = Application
        fields = ('status', 'id')

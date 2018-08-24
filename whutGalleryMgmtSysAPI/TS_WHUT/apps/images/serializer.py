from rest_framework import serializers
from .models import ImageModel, BannerModel, Comment, SearchWord, SmallGroups, GroupImage, Groups
from django.contrib.auth import get_user_model
from operations.models import LikeShip, UserFolderImage, Follow, CommentLike
from users.models import UserMessage

User = get_user_model()


class SearchWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchWord
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerModel
        fields = ('image', 'url', 'title')


class BannerOneSerializer(serializers.ModelSerializer):
    class Meta:
        module = BannerModel
        fields = ('id', 'desc')


class UserBrifSerializer(serializers.ModelSerializer):
    upload_nums = serializers.SerializerMethodField()

    def get_upload_nums(self, obj):
        return ImageModel.objects.filter(user=obj, if_active=True).count()

    class Meta:
        model = User
        fields = ('image', 'id', 'username', 'upload_nums', 'fan_nums')


class ImageSerializer(serializers.ModelSerializer):
    user = UserBrifSerializer()
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()
    if_collect = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        # 图片大小
        return obj.image.size

    def get_image(self, obj):
        # 图片链接
        return 'http://' + self.context['request']._request.META['HTTP_HOST'] + obj.image['avatar'].url

    def get_if_like(self, obj):
        # 是否点赞图片
        if not self.context['request'].user.is_authenticated:
            return False
        ship = LikeShip.objects.filter(user_id=self.context['request'].user.id, image_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_if_collect(self, obj):
        # 是否收藏图片
        if not self.context['request'].user.is_authenticated:
            return False
        ship = UserFolderImage.objects.filter(user_id=self.context['request'].user.id, image_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_if_follow(self, obj):
        # 是否关注上传者
        if not self.context['request'].user.is_authenticated:
            return False
        ship = Follow.objects.filter(fan_id=self.context['request'].user.id, follow_id=obj.user.id)
        if ship.count():
            return ship[0].id
        return False

    def get_height(self, obj):
        # 图片高
        return obj.image.height

    def get_width(self, obj):
        # 图片宽
        return obj.image.width

    class Meta:
        model = ImageModel
        fields = '__all__'


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    cates = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['image'].size > 10485760:
            raise serializers.ValidationError("图片过大")
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = ImageModel
        fields = ('desc', 'cates', 'name', 'image')


class CommentListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()
    user = UserBrifSerializer()
    reply = serializers.SerializerMethodField()

    def get_reply(self, obj):
        if obj.reply:
            return obj.reply.username
        return None

    def get_if_like(self, obj):
        # 是否点赞
        user = self.context['request'].user
        ship = CommentLike.objects.filter(user_id=user.id, comment_id=obj.id)
        if ship.count():
            return ship[0].id
        return False

    def get_image(self, obj):
        # 验证参数
        image = self.context['request'].query_params.get('image')
        if image:
            return int(image)
        raise serializers.ValidationError('参数错误!')

    class Meta:
        model = Comment
        fields = '__all__'


class SmallGroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmallGroups
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    groups = SmallGroupListSerializer(many=True)

    class Meta:
        model = Groups
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs['is_add_info'] == 'false' or not attrs['is_add_info']:
            attrs['is_add_info'] = False
        elif attrs['is_add_info']:
            attrs['is_add_info'] = True

        if not attrs['is_add_info']:
            if attrs['floor'] > 0:
                raise serializers.ValidationError('不是回复,不应该有楼层数')
            else:
                comments = Comment.objects.filter(image=attrs['image'], is_add_info=False)
                if comments.count():
                    floor = comments.order_by("-floor")[0].floor
                    attrs['floor'] = floor + 1
                else:
                    attrs['floor'] = 1
        else:
            if attrs['floor'] == 0:
                raise serializers.ValidationError('回复应该有楼层数')
            reply = attrs['reply']
            UserMessage(post_user=self.context['request'].user.username, user=reply, message=attrs['content']).save()
        return attrs

    class Meta:
        model = Comment
        fields = ('image', 'user', 'reply', 'content', 'is_add_info', 'floor', 'id')

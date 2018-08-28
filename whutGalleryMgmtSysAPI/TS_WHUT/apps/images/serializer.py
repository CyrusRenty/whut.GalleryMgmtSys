from rest_framework import serializers
from .models import ImageModel, BannerModel, Comment, SearchWord, Groups
from django.contrib.auth import get_user_model
from operations.models import LikeShip, UserFolderImage, Follow, CommentLike
from users.models import UserMessage
import jieba
from django.db.models import Q

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
        return ImageModel.objects.filter(user=obj, if_active=1).count()

    class Meta:
        model = User
        fields = ('image', 'id', 'username', 'upload_nums', 'fan_nums')


def recommend_image(desc):
    """
    根据图片详情推荐图片
    :param desc: 图片描述
    :return: queryset
    """
    rows = ('cates', 'name', 'desc', 'user__username')
    q = Q()
    q.connector = 'OR'
    for row in rows:
        kws = jieba.cut_for_search(desc)
        for kw in kws:
            q.children.append((row + '__icontains', kw))
    return ImageModel.objects.filter(q)


class ImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('desc', 'cates', 'name', 'image')


class ImageSerializer(serializers.ModelSerializer):
    user = UserBrifSerializer()
    image = serializers.SerializerMethodField()
    if_like = serializers.SerializerMethodField()
    if_collect = serializers.SerializerMethodField()
    if_follow = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    recommend = serializers.SerializerMethodField()

    def get_size(self, obj):
        # 图片大小
        return obj.image.size

    def get_recommend(self, obj):
        """推荐图片"""
        # 如果不是图片详情
        data = []
        if not self.context.get('water_image'):
            return data
        images = recommend_image(obj.desc)
        for image in images[:5]:
            data.append({
                'id': image.id,
                "image": image.image['avatar'].url
            })
        return data

    def get_image(self, obj):
        # 图片链接
        if self.context.get('water_image'):
            return '/media/main/' + obj.image.url.rsplit('/', 1)[1]
        return obj.image['avatar'].url

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
        exclude = ('ori_img', 'file', 'if_active')


class ImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    cates = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['image'].size > 10485760:
            raise serializers.ValidationError("预览图过大")
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = ImageModel
        fields = ('desc', 'cates', 'name', 'image', 'file', 'ori_img')


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


class GroupListSerializer(serializers.ModelSerializer):
    kids = serializers.SerializerMethodField()

    def get_kids(self, obj):
        show = self.context['request'].query_params.get('show')
        data = []
        if show == 'true':
            kids = Groups.objects.filter(parent=obj)
        else:
            kids = Groups.objects.filter(parent=obj, if_show=True)

        for kid in kids:
            kid_data = []

            if show == 'true':
                kid_kids = Groups.objects.filter(parent=kid)
            else:
                kid_kids = Groups.objects.filter(parent=kid, if_show=True)
            if kid_kids.count():
                for kid_kid in kid_kids:
                    kid_data.append({
                        "name": kid_kid.name,
                        "id": kid_kid.id,
                    })

            data.append({
                "name": kid.name,
                "id": kid.id,
                "kids": kid_data
            })
        return data

    class Meta:
        model = Groups
        fields = ('name', 'id', 'kids')


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

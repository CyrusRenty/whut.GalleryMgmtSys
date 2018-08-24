import xadmin

from .models import Follow, LikeShip, DownloadShip, CommentLike, UserFolderImage, Application, Report


class FollowAdmin(object):
    list_display = ('follow', 'fan', 'add_time')
    list_filter = ('follow', 'fan', 'add_time')
    readonly_fields = ('add_time', 'fan', 'follow')
    model_icon = 'fa fa-heart'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class LikeShipAdmin(object):
    list_display = ('user', 'image', 'add_time')
    list_filter = ('user', 'image', 'add_time')
    readonly_fields = ('user', 'image', 'add_time')
    model_icon = 'fa fa-thumbs-o-up'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class DownloadShipAdmin(object):
    list_display = ('user', 'image', 'add_time')
    list_filter = ('user', 'image', 'add_time')
    readonly_fields = ('user', 'image', 'add_time')
    model_icon = 'fa fa-download'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class CommentLikeAdmin(object):
    list_display = ('comment', 'user', 'add_time')
    list_filter = ('comment', 'user', 'add_time')
    readonly_fields = ('user', 'add_time')
    model_icon = 'fa fa-thumbs-up'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class UserFolderImageAdmin(object):
    list_display = ('folder', 'user', 'image', 'add_time')
    list_filter = ('folder', 'user', 'image', 'add_time')
    readonly_fields = ('folder', 'user', 'image', 'add_time')
    model_icon = 'fa fa-gratipay'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class ApplicationAdmin(object):
    list_display = ('user', 'status', 'url')
    list_filter = ('user', 'status')
    readonly_fields = ('user', 'status')
    model_icon = 'fa fa-plus-circle'
    refresh_times = (5, 10)

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class ReportAdmin(object):
    list_display = ('user', 'status', 'reason', 'content', 'add_time')
    list_filter = ('status', 'reason', 'add_time')
    readonly_fields = ('user', 'add_time')
    model_icon = 'fa fa-flag'
    refresh_times = (5, 10)

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

xadmin.site.register(Follow, FollowAdmin)
xadmin.site.register(LikeShip, LikeShipAdmin)
xadmin.site.register(DownloadShip, DownloadShipAdmin)
xadmin.site.register(CommentLike, CommentLikeAdmin)
xadmin.site.register(UserFolderImage, UserFolderImageAdmin)
xadmin.site.register(Application, ApplicationAdmin)
xadmin.site.register(Report, ReportAdmin)

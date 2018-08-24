import xadmin
from xadmin.layout import Main, Fieldset, Side

from .models import BannerModel, ImageModel, GroupImage, Comment, SmallGroups, Groups


class GroupsAdmin(object):
    list_display = ('name', 'add_time', 'if_show')
    search_fields = ('name',)
    list_filter = ('name', 'add_time', 'if_show')
    model_icon = 'fa fa-object-group'
    form_layout = (
        Main(
            Fieldset('',
                     'name', 'add_time',
                     css_class='unsort no_title'
                     ),
        ),
        Side(
            Fieldset('状态',
                     'if_show'
                     ),
        )
    )


class SmallGroupsAdmin(object):
    list_display = ('name', 'add_time', 'group')
    search_fields = ('name',)
    list_filter = ('name', 'add_time')
    model_icon = 'fa fa-object-group'


class BannerModelAdmin(object):
    list_display = ('title', 'url', 'if_show', 'add_time')
    search_fields = ('title',)
    list_filter = ('title', 'if_show', 'add_time')
    model_icon = 'fa fa-picture-o'
    form_layout = (
        Main(
            Fieldset('',
                     'title', 'image', 'url', 'add_time', 'index',
                     css_class='unsort no_title'
                     ),
        ),
        Side(
            Fieldset('状态',
                     'if_show'
                     ),
        )
    )
    style_fields = {"desc": "ueditor"}


class ImageModelAdmin(object):
    list_display = ('name', 'user', 'if_active', 'desc', 'pattern', 'cates', 'add_time')
    search_fields = ('name', 'desc', 'pattern')
    list_filter = ('user', 'name', 'if_active', 'desc', 'pattern', 'cates', 'add_time')
    readonly_fields = ('user', 'add_time')
    model_icon = 'fa fa-file-image-o'
    refresh_times = (5, 10)
    relfield_style = 'fk-ajax'

    form_layout = (
        Main(
            Fieldset('',
                     'name', 'image', 'user', 'pattern', 'desc', 'cates',
                     css_class='unsort no_title'
                     ),
        ),
        Side(
            Fieldset('状态',
                     'if_active'
                     ),
        )
    )

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


# class GroupImageAdmin(object):
#     list_display = ('name', 'image', 'add_time')
#     search_fields = ('name', 'image')
#     list_filter = ('name', 'image', 'add_time')
#     model_icon = 'fa fa-object-group'


class CommentAdmin(object):
    list_display = ('content', 'like', 'image', 'user', 'reply', 'add_time', 'num')
    search_fields = ('content',)
    list_filter = ('content', 'like', 'image', 'user', 'reply', 'add_time')
    readonly_fields = ('content', 'user', 'reply', 'add_time', 'like')
    model_icon = 'fa fa-commenting-o'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

xadmin.site.register(BannerModel, BannerModelAdmin)
xadmin.site.register(ImageModel, ImageModelAdmin)
# xadmin.site.register(GroupImage, GroupImageAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(SmallGroups, SmallGroupsAdmin)
xadmin.site.register(Groups, GroupsAdmin)

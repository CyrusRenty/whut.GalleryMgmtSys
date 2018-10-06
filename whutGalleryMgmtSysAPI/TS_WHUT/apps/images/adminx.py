import xadmin
from xadmin.layout import Main, Fieldset, Side

from .models import BannerModel, ImageModel, Comment, Groups, SearchWord, GroupImage


class SearchWordAdmin(object):
    list_display = ('word', 'add_time', 'num')
    search_fields = ('word',)
    list_filter = ('num', 'add_time')
    model_icon = 'fa fa-file-word-o'


class GroupImageAdmin(object):
    list_display = ('group', 'image', 'add_time')
    list_filter = ('group',)
    model_icon = 'fa fa-object-group'


class GroupsAdmin(object):
    list_display = ('name', 'add_time', 'if_show', 'level', 'parent')
    search_fields = ('name',)
    list_filter = ('name', 'add_time', 'if_show', 'level')
    model_icon = 'fa fa-object-group'
    list_editable = ('name', 'if_show')
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


class BannerModelAdmin(object):
    list_display = ('title', 'url', 'if_show', 'add_time')
    search_fields = ('title',)
    list_filter = ('title', 'if_show', 'add_time')
    model_icon = 'fa fa-picture-o'
    list_editable = ('if_show',)
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
    list_display = ('name', 'url', 'if_active', 'cates', 'pattern', 'i_desc', 'add_time')
    search_fields = ('name', 'desc', 'pattern')
    list_filter = ('user', 'name', 'if_active', 'desc', 'pattern', 'cates', 'add_time')
    readonly_fields = ('add_time',)
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
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Groups, GroupsAdmin)
xadmin.site.register(SearchWord, SearchWordAdmin)
xadmin.site.register(GroupImage, GroupImageAdmin)

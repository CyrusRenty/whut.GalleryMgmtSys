import xadmin
from xadmin import views
from xadmin.layout import Main, Fieldset, Row, Side

from .models import UserProfile, EmailVerifyRecord, Folder, UserMessage, Org


@xadmin.sites.register(views.website.IndexView)
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "欢迎面板",
             "content": "<h3> 欢迎来到图说理工后台! </h3><p>有问题请联系: <br/>张志强QQ : 2310091880</p>"},
            {"type": "qbutton", "title": "快速开始",
             "btns": [{"title": "上传图片", "url": '/admin/images/imagemodel/add/'},
                      {"title": "新建用户", "url": '/admin/users/userprofile/add/'}]},
            {"type": "list", "model": "images.ImageModel", "title": "等待审核图片", "params": {"_p_if_active": False}},
        ],
        [
            {"type": "list", "model": "operations.Application", "title": "等待审核用户", "params": {"_p_status": 2}},
            {"type": "list", "model": "users.Org", "title": "等待认证机构", "params": {"_p_status": 1}},
            {"type": "list", "model": "operations.Report", "title": "等待审查举报", "params": {"_p_status": 1}},
        ]
    ]


@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    site_title = "图说理工后台管理系统"
    site_footer = "图说理工在线网"
    menu_style = "accordion"


class UserProfileAdmin(object):
    list_display = ('username', 'email', 'is_staff', 'mobile', 'number', 'gender', 'birthday')
    search_fields = ('number', 'email', 'username', 'mobile')
    list_filter = ('is_staff',)
    model_icon = 'fa fa-user-o'
    readonly_fields = ('follow_nums', 'fan_nums', 'upload_nums', 'like_nums',
                       'collection_nums', 'download_nums', 'add_time', 'password')
    relfield_style = 'fk-ajax'
    form_layout = (
        Main(
            Fieldset('',
                     'username', 'password',
                     css_class='unsort no_title'
                     ),
            Fieldset('关键信息',
                     Row('real_name', 'p_class'),
                     Row('email', 'mobile'),
                     Row('qq', 'id_card'),
                     ),
            Fieldset('权限',
                     'groups', 'user_permissions'
                     ),
            Fieldset('日期',
                     'last_login', 'date_joined'
                     ),
        ),
        Side(
            Fieldset('状态',
                     'is_active', 'is_staff', 'is_superuser', 'if_sign'
                     ),
        )
    )

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class EmailVerifyRecordAdmin(object):
    list_display = ('send_type', 'code', 'send_email', 'send_time')
    search_fields = ('send_email', 'code')
    list_filter = ('send_time', 'send_type')
    model_icon = 'fa fa-envelope-o'
    readonly_fields = ('send_time', 'send_type', 'send_email')

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class FolderAdmin(object):
    list_display = ('name', 'user', 'nums', 'add_time')
    search_fields = ('name',)
    list_filter = ('user', 'add_time')
    model_icon = 'fa fa-folder-o'
    readonly_fields = ('user', 'nums', 'add_time')
    relfield_style = 'fk-ajax'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class OrgAdmin(object):
    list_display = ('name', 'status', 'user', 'teacher', 'add_time')
    search_fields = ('name', 'teacher')
    list_filter = ('name', 'add_time', 'status')
    readonly_fields = ('add_time', 'user')
    relfield_style = 'fk-ajax'
    model_icon = 'fa fa-sitemap'

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


class UserMessageAdmin(object):
    list_display = ('message', 'user', 'post_user', 'has_read', 'add_time')
    search_fields = ('message',)
    list_filter = ('user', 'post_user', 'has_read', 'add_time')
    model_icon = 'fa fa-comment-o'
    readonly_fields = ('add_time', 'user', 'post_user')

    form_layout = (
        Main(
            Fieldset('',
                     'message', 'user', 'post_user', 'add_time',
                     css_class='unsort no_title'
                     ),
        ),
        Side(
            Fieldset('状态',
                     'has_read'
                     ),
        )
    )

    def get_readonly_fields(self):
        if self.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Folder, FolderAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(Org, OrgAdmin)

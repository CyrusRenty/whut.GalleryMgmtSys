# 图说理工

## 介绍

前端使用 Vue 框架、后台使用 Django-rest-framework 框架。Django-rest-framework 是一个针对 RESTful API 设计的后端框架，其基于 Django 框架，Django 框架是一个 MVC 模式的 Web 框架，Django-rest-framework 与 Vue 的结合，则是 MVC 与 MVVM 的结合，在后端抛弃了 V 视图层，使用 Vue 来补充，保留的 C 控制层则用来实现父级路由和数据逻辑控制。后台管理界面则是使用 Django 强大的 Admin 后台系统。完全解放了前端，使得 Vue 完全被用在客户端。

## 项目前台

## 项目后台及其他

| 环境 | Python3.6 |
| :---: | :---: |
| 后台框架 | Django-rest-framework |
| 数据库 | MySQL |
| 服务器 | Nginx |

### 介绍
| 模块 | 简介 |
| :---: | :---: |
| images | 处理有关图片的 API 包括图片的删改查、推荐、点赞、评论、水印等 |
| users | 处理有关用户的 API 包括用户的删改查、组织认证、收藏夹操作等 |
| operations | 处理有关用户操作的 API 包括注册、登录、点赞、收藏、评论、下载等 |


### 后台文件路径/目录

[whutGalleryMgmtSysAPI/**TS_WHUT**](https://github.com/Terry-Ren/whut.GalleryMgmtSys/tree/master/whutGalleryMgmtSysAPI '项目后台')

- **TS_WHUT**
    - apps `(应用程序)`
        - images
            - `__init__.py`
            - `adminx.py`
            - `apps.py`
            - `filters.py`
            - `models.py`
            - `serializer.py`
            - `signals.py`
            - `views.py`
        - operations `(同上)`
        - users `(同上)`
        - my_utils `(帮助函数)`
            - `add_wa.py`
            - `read_file.py`
            - `send_email.py`
            - `storage.py`
    - extra_appps `(引入的app)`
    - conf `(配置文件夹)` 
    - static `(静态文件夹)`
    - media `(媒体文件夹)`
    - templates `(模板文件夹)`
        - `active_fail.html`
        - `images.html`
        - `password_reset.html`
    - TS_WHUT
        - `__init__.py`
        - `settings.py`
        - `url.py`
        - `wsgi.py`
    - `manage.py`

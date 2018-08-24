#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# send_email.py
"""
模块功能: 发送邮件
"""
__author__ = 'Aiyane'

from random import Random  # 随机数
from django.core.mail import send_mail  # 引入发送邮件方法

from users.models import EmailVerifyRecord  # 引入邮箱验证表单
from TS_WHUT.settings import EMAIL_FROM  # 引入配置中的发送人


def random_str(randomlength=8):
    """
    这是一个随机验证码生成(random_str)的方法，接受一个int类型的参数，
    返回一个在'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    中产生的随机字串，字串长度为该参数数值，参数默认值为8,注意：最长不超过62位！
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type="register"):
    """
    email: 目标邮箱
    send_type: 相应类型，默认为注册(register)类型
    """
    email_record = EmailVerifyRecord()

    # 设置密码长度
    # if send_type == "update_email":
    #     code = random_str(4)
    # else:
    code = random_str(16)

    # 将每一次发的邮件内容保存在数据库中
    email_record.code = code  # 将随机验证码存入邮箱验证表单中的验证码(code)类
    email_record.send_email = email
    email_record.send_type = send_type  # 看清楚models.py中send_type的相关类型
    email_record.save()

    if send_type == "register":
        email_title = "图说理工网用户激活链接"
        email_body = "请点击下面的链接激活你的账号：http://111.231.230.54/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "图说理工网网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://111.231.230.54/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    # elif send_type == "update_email":
    #     email_title = "图说理工网邮箱修改验证码"
    #     email_body = "你的邮箱验证码为：{0}".format(code)
    #
    #     send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    #     if send_status:
    #         pass

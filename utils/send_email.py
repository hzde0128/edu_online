from users.models import EmailVerifyCode
from random import randrange
from admin.settings import EMAIL_FROM
from django.core.mail import send_mail


def get_random_code(code_length):
    """
    从码源中随机获取随机码进行拼接并返回
    @params: code_length： 根据指定长度生成随机码
    @return code 返回指定长度的随机码
    """
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        # 随机选择一个字符
        str1 = code_source[randrange(0, len(code_source)-1)]
        code += str1
    return code


def send_mail_code(email, send_type):
    """
    创建邮箱验证码对象，保存到数据库，用来做对比
    @params: email邮件发送对象
    @params: send_type: 邮件发送类型
    """
    code = get_random_code(16)
    a = EmailVerifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()

    # 发送邮件
    if send_type == 1:
        subject = '[在线教育网]欢迎注册'
        message = '请点击以下链接激活您的账号：\nhttp://127.0.0.1:8000/users/user_active/' + code
        send_mail(subject, message, EMAIL_FROM, [email])
    if send_type == 2:
        subject = '[在线教育网]重置密码'
        message = '请点击以下链接重置您的密码：\nhttp://127.0.0.1:8000/users/user_reset/' + code
        send_mail(subject, message, EMAIL_FROM, [email])
    if send_type == 3:
        subject == '[在线教育网]更换邮箱'
        message = '您的邮箱验证码是：' + code
        send_mail(subject, message, EMAIL_FROM, [email])



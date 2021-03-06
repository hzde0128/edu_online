from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    UserProfile 集成自AbstractUser
    用户表字段定义
    """
    image = models.ImageField(upload_to='users/%y/%m/%d', default='default.jpg', max_length=200, verbose_name="用户头像")
    nick_name = models.CharField(max_length=20, verbose_name="用户昵称", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="用户生日")
    gender = models.CharField(choices=(('男', '男'), ('女', '女')), verbose_name="用户性别", max_length=6, default='男')
    address = models.CharField(max_length=300, verbose_name="用户地址", null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="用户手机")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.username

    def get_msg_counter(self):
        """
        未读消息需要在用户登录后所有页面展示
        定义一个方法获取用户未读消息
        """
        from operations.models import UserMessage
        counter = UserMessage.objects.filter(msg_user=self.id, msg_status=False).count()
        return counter

    class Meta:
        db_table = 'edu_users'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class BannerInfo(models.Model):
    """
    BannerInfo 轮播图表字段定义
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banners/%y/%m', max_length=200, verbose_name="轮播图片")
    url = models.URLField(max_length=200, verbose_name='轮播链接')
    index = models.IntegerField(default=100, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'edu_banners'
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name


class EmailVerifyCode(models.Model):
    """
    EmailVerifyCode 邮箱验证码表字段定义
    """
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    code = models.CharField(max_length=20, verbose_name="验证码")
    send_type = models.IntegerField(choices=((1, '注册激活'), (2, '重置密码'), (3, '修改邮箱')), verbose_name="发送类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'edu_email_verify_code'
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserProfile(AbstractUser):
    """
    UserProfile 集成自AbstractUser
    用户表字段定义
    """
    image = models.ImageField(upload_to='users/%y/%m/%d', max_length=200, verbose_name="用户头像", null=True, blank=True)
    nick_name = models.CharField(max_length=20, verbose_name="用户昵称", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True, verbose_name="用户生日")
    gender = models.CharField(choices=(('男', '男'), ('女', '女')), verbose_name="用户性别", max_length=6, default='男')
    address = models.CharField(max_length=300, verbose_name="用户地址", null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name="用户手机")
    is_start = models.BooleanField(default=False, verbose_name="是否激活")
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
    image = models.ImageField(upload_to='banners/%y/%m/%d',max_length=200,verbose_name="轮播图片")
    url = models.URLField(max_length=200,verbose_name='轮播链接')
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    def __str__(self):
        return str(self.image)

    class Meta:
        db_table = 'edu_banners'
        verbose_name = '轮播图信息'
        verbose_name_plural = verbose_name


class EmailVerifyCode(models.Model):
    """
    EmailVerifyCode 邮箱验证码表字段定义
    """
    email = models.EmailField(max_length=50,verbose_name="邮箱")
    code = models.CharField(max_length=20,verbose_name="验证码")
    send_type = models.CharField(choices=(('register','注册激活'),('forget','重置密码'),('change','修改邮箱')),max_length=15,verbose_name="发送类别")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'edu_email_verify_code'
        verbose_name='邮箱验证码'
        verbose_name_plural = verbose_name

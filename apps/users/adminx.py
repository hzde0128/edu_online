import xadmin
from xadmin import views
from .models import BannerInfo, EmailVerifyCode


class BaseAdminView(object):
    """
    BaseAdminView 全局配置
    启用主题功能
    """
    enable_themes = True
    use_bootswatch = True


class CommAdminView(object):
    """
    CommAdminView 通用配置
    accordion 手风琴折叠效果
    可以设置xadmin标题和底部信息
    """
    menu_style = 'accordion'
    site_title = '在线教育网'
    site_footer = '2020 版权所有'


class BannerInfoXadmin(object):
    """
    BannerInfoXadmin 后台显示字段列表
    """
    list_display = ['image', 'url', 'add_time']
    model_icon = 'fa fa-picture-o'


class EmailVerifyCodeXadmin(object):
    """
    EmailVerifyCodeXadmin 后台显示字段列表
    """
    list_display = ['email', 'code', 'send_type', 'add_time']
    model_icon = 'fa fa-envelope-o'


xadmin.site.register(views.BaseAdminView, BaseAdminView)
xadmin.site.register(views.CommAdminView, CommAdminView)
xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)

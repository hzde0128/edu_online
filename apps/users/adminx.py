import xadmin
from xadmin import views
from .models import BannerInfo, EmailVerifyCode


class BaseAdminView(object):
    # 启用主题功能
    enable_themes = True
    use_bootswatch = True


class CommAdminView(object):
    # 代码折叠
    menu_style = 'accordion'
    site_title = '在线教育网'
    site_footer = '2020 版权所有'


class BannerInfoXadmin(object):
    list_display = ['image', 'url', 'add_time']
    model_icon = 'fa fa-picture-o'


class EmailVerifyCodeXadmin(object):
    list_display = ['email', 'code', 'send_type', 'add_time']
    model_icon = 'fa fa-envelope-o'


xadmin.site.register(views.BaseAdminView, BaseAdminView)
xadmin.site.register(views.CommAdminView, CommAdminView)
xadmin.site.register(BannerInfo, BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode, EmailVerifyCodeXadmin)

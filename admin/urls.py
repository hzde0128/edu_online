"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve
# from django.contrib import admin
import xadmin
import DjangoUeditor
from users.views import IndexView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView, name='index'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'xadmin/', xadmin.site.urls),
    url(r'^users/', include(('users.urls', 'users'), namespace='users.urls')),
    url(r'^orgs/', include(('orgs.urls', 'orgs'), namespace='orgs.urls')),
    url(r'^courses/', include(('courses.urls', 'courses'), namespace='courses.urls')),
    url(r'^operations/', include(('operations.urls', 'operations'), namespace='operations.urls')),
    url(r'media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT, }),
]

handler404 = 'users.views.handler_404'
handler500 = 'users.views.handler_500'

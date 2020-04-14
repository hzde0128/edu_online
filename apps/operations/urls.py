from django.conf.urls import url

from operations import views


urlpatterns = [
    url(r'user_ask/$', views.UserAsk.as_view(), name='user_ask'),
    url(r'user_love/$', views.UserLove.as_view(), name='user_love'),
    url(r'user_delete_love/$', views.UserDeleteLove.as_view(), name='user_delete_love'),
    url(r'user_comment/$', views.UserComment.as_view(), name='user_comment'),
]

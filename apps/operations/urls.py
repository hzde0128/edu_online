from django.conf.urls import url
from .views import user_ask, user_love, user_delete_love, user_comment


urlpatterns = [
    url(r'user_ask/$', user_ask, name='user_ask'),
    url(r'user_love/$', user_love, name='user_love'),
    url(r'user_delete_love/$', user_delete_love, name='user_delete_love'),
    url(r'user_comment/$', user_comment, name='user_comment'),
]

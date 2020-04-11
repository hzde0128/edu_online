from django.conf.urls import url
from .views import user_register, user_login, user_forget, user_logout, user_active, user_reset, \
    user_info, avator_upload, update_info, update_email, reset_email, user_info_course, \
    user_info_fav_org, user_info_fav_course, user_info_fav_teacher, user_info_message, \
    user_info_message_read

urlpatterns = [
    url(r'user_register/$', user_register, name='user_register'),
    url(r'user_login/$', user_login, name='user_login'),
    url(r'user_forget/$', user_forget, name='user_forget'),
    url(r'user_info/$', user_info, name='user_info'),
    url(r'user_info/course$', user_info_course, name='user_info_course'),
    url(r'user_logout/$', user_logout, name='user_logout'),
    url(r'user_active/(\w+)/$', user_active, name='user_active'),
    url(r'user_reset/(\w+)/$', user_reset, name='user_reset'),
    url(r'avator_upload/$', avator_upload, name='avator_upload'),
    url(r'update_info/$', update_info, name='update_info'),

    url(r'update_email/$', update_email, name='update_email'),
    url(r'reset_email/$', reset_email, name='reset_email'),

    url(r'user_info/fav/org$', user_info_fav_org, name='user_info_fav_org'),
    url(r'user_info/fav/course$', user_info_fav_course, name='user_info_fav_course'),
    url(r'user_info/fav/teacher$', user_info_fav_teacher, name='user_info_fav_teacher'),
    url(r'user_info/message$', user_info_message, name='user_info_message'),
    url(r'user_info/message_read$', user_info_message_read, name='user_info_message_read'),
]

from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'user_register/$', views.UserRegister.as_view(), name='user_register'),
    url(r'user_login/$', views.UserLogin.as_view(), name='user_login'),
    url(r'user_forget/$', views.UserForget.as_view(), name='user_forget'),
    url(r'user_info/$', views.UserInfo.as_view(), name='user_info'),
    url(r'user_info/course$', views.UserInfoCourse.as_view(), name='user_info_course'),
    url(r'user_logout/$', views.UserLogout.as_view(), name='user_logout'),
    url(r'user_active/(\w+)/$', views.UserActive.as_view(), name='user_active'),
    url(r'user_reset/$', views.UserReset.as_view(), name='user_reset'),
    url(r'avator_upload/$', views.AvatarUpload.as_view(), name='avatar_upload'),
    url(r'update_info/$', views.UpdateInfo.as_view(), name='update_info'),

    url(r'update_email/$', views.UpdateEmail.as_view(), name='update_email'),
    url(r'reset_email/$', views.ResetEmail.as_view(), name='reset_email'),
    # 个人中心
    url(r'user_info/fav/org$', views.UserInfoFavOrg.as_view(), name='user_info_fav_org'),
    url(r'user_info/fav/course$', views.UserInfoFavCourse.as_view(), name='user_info_fav_course'),
    url(r'user_info/fav/teacher$', views.UserInfoFavTeacher.as_view(), name='user_info_fav_teacher'),
    url(r'user_info/message$', views.UserInfoMessage.as_view(), name='user_info_message'),
    url(r'user_info/message_read$', views.UserInfoMessageRead.as_view(), name='user_info_message_read'),
]

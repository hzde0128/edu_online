from django.conf.urls import url

from courses import views

urlpatterns = [
    url(r'course_list', views.CourseList.as_view(), name='course_list'),
    url(r'course_detail/(\d+)', views.CourseDetail.as_view(), name='course_detail'),
    url(r'course_video/(\d+)', views.CourseVideo.as_view(), name='course_video'),
    url(r'course_comment/(\d+)', views.CourseComment.as_view(), name='course_comment'),
    url(r'course_play/(\d+)', views.VideoPlay.as_view(), name='course_play'),
]

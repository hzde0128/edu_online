from django.conf.urls import url

from .views import course_list, course_detail, course_video, course_comment


urlpatterns = [
    url(r'course_list', course_list, name='course_list'),
    url(r'course_detail/(\d+)', course_detail, name='course_detail'),
    url(r'course_video/(\d+)', course_video, name='course_video'),
    url(r'course_comment/(\d+)', course_comment, name='course_comment')
]

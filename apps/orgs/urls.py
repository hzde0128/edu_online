from django.conf.urls import url

from orgs import views

urlpatterns = [
    url(r'org_list/$', views.OrgList.as_view(), name='org_list'),
    url(r'org_detail/(\d+)/$', views.OrgDetail.as_view(), name='org_detail'),
    url(r'org_detail_course/(\d+)/$', views.OrgDetailCourse.as_view(), name='org_detail_course'),
    url(r'org_detail_desc/(\d+)/$', views.OrgDetailDesc.as_view(), name='org_detail_desc'),
    url(r'org_detail_teacher/(\d+)/$', views.OrgDetailTeacher.as_view(), name='org_detail_teacher'),

    url(r'teacher_list/$', views.TeacherList.as_view(), name='teacher_list'),
    url(r'teacher_detail/(\d+)$', views.TeacherDetail.as_view(), name='teacher_detail')
]

import xadmin
from .models import CityInfo, OrgInfo, TeacherInfo


# Create your models here.
class CityInfoXadmin(object):
    list_dispaly = ['name', 'add_time']
    model_icon = 'fa fa-list'


class OrgInfoXadmin(object):
    list_display = ['name', 'image', 'study_num', 'address', 'org_category', 'desc', 'course_num', 'love_num', 'city', 'add_time']
    model_icon = 'fa fa-sitemap'
    style_fields = {'detail': 'ueditor'}

class TeacherInfoXadmin(object):
    list_display = ['name', 'image', 'age', 'work_year', 'work_position', 'work_style', 'click_num', 'love_num', 'org', 'add_time']
    model_icon = 'fa fa-user-o'


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
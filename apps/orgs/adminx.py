import xadmin
from .models import CityInfo, OrgInfo, TeacherInfo


# Create your models here.
class CityInfoXadmin(object):
    list_dispaly = ['name', 'add_time']
    model_icon = 'fa fa-list'


class OrgInfoXadmin(object):
    list_display = ['name', 'image', 'study_num', 'address', 'org_category', 'desc', 'click_num', 'love_num', 'city', 'add_time']
    model_icon = 'fa fa-sitemap'
    readonly_fields = ['love_num', 'click_num', 'study_num']
    style_fields = {'detail': 'ueditor'}


class TeacherInfoXadmin(object):
    list_display = ['name', 'image', 'age', 'work_year', 'work_position', 'work_style', 'click_num', 'love_num', 'org', 'add_time']
    readonly_fields = ['love_num', 'click_num']
    model_icon = 'fa fa-leaf'


xadmin.site.register(CityInfo, CityInfoXadmin)
xadmin.site.register(OrgInfo, OrgInfoXadmin)
xadmin.site.register(TeacherInfo, TeacherInfoXadmin)
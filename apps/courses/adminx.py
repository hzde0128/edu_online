import xadmin
from .models import CourseInfo, LessonInfo, VideoInfo, SourceInfo

# Create your models here.
class CourseInfoXadmin(object):
    list_display = ['name', 'image', 'study_num', 'love_num', 'desc', 'study_num', 'comment_num', 'level',
                    'course_category', 'click_num', 'org', 'teacher']
    model_icon = 'fa fa-film'


class LessonInfoXadmin(object):
    list_display = ['name', 'course', 'add_time']
    model_icon = 'fa fa-list'


class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url', 'lesson', 'add_time']
    model_icon = 'fa fa-play-circle-o'


class SourceInfoXadmin(object):
    list_display = ['name', 'download', 'course', 'add_time']
    model_icon = 'fa fa-file-text'

xadmin.site.register(CourseInfo, CourseInfoXadmin)
xadmin.site.register(LessonInfo, LessonInfoXadmin)
xadmin.site.register(VideoInfo, VideoInfoXadmin)
xadmin.site.register(SourceInfo, SourceInfoXadmin)

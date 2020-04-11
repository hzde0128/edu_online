import xadmin
from .models import UserLove, UserCourse, UserAsk, UserComment, UserMessage

class UserLoveXadmin(object):
    list_display = ['love_man', 'love_id', 'love_type', 'love_type', 'add_time']
    model_icon = 'fa fa-heart'

class UserCourseXadmin(object):
    list_display = ['study_man', 'study_course', 'add_time']
    model_icon = 'fa fa-television'

class UserAskXadmin(object):
    list_display = ['name', 'phone', 'course', 'add_time']
    model_icon = 'fa fa-question-circle-o'

class UserCommentXadmin(object):
    list_display = ['comment_man', 'comment_course', 'content', 'add_time']
    model_icon = 'fa fa-comment-o'

class UserMessageXadmin(object):
    list_display = ['msg_user', 'msg_content', 'msg_status', 'add_time']
    model_icon = 'fa fa-comments-o'

xadmin.site.register(UserLove, UserLoveXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)
xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(UserComment, UserCommentXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
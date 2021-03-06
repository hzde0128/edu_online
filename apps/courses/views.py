from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import View

from .models import CourseInfo, VideoInfo
from operations.models import UserLove, UserCourse
from utils.decorators import login_decorator


# Create your views here.
class CourseList(View):
    """
    CourseList 课程列表展示
    """
    def get(self, request):
        courses = CourseInfo.objects.all()
        recommend = courses.order_by('-add_time')[:3]

        # 全局搜索过滤,模糊搜索
        keyword = request.GET.get('keyword', '')
        if keyword:
            courses = courses.filter(
                Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(detail__icontains=keyword))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            courses = courses.order_by('-'+sort)
        else:
            courses = courses.order_by('-add_time')

        # 分页
        page = request.GET.get('page')
        pa = Paginator(courses, 3)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'courses/course-list.html', {
            'courses': courses,
            'recommend': recommend,
            'pages': pages,
            'sort': sort,
            'keyword': keyword,
        })


class CourseDetail(View):
    """
    CourseDetail 课程详情
    """
    def get(self, request, course_id):
        if course_id:
            course = CourseInfo.objects.filter(id=course_id)[0]
            recommend = CourseInfo.objects.filter(course_category=course.course_category).exclude(id=course_id)

            course.click_num += 1
            course.save()

            love_course = False
            love_org = False
            if request.user.is_authenticated:
                love = UserLove.objects.filter(love_id=course_id, love_type=2, love_status=True, love_man=request.user)
                if love:
                    love_course = True
                love = UserLove.objects.filter(love_id=course.org.id, love_type=1,
                                               love_status=True, love_man=request.user)
                if love:
                    love_org = True
            if course:
                return render(request, 'courses/course-detail.html', {
                    'course': course,
                    'recommend': recommend,
                    'love_course': love_course,
                    'love_org': love_org,
                })


class VideoPlay(View):
    """
    CourseVideo 课程学习
    """
    @login_decorator
    def get(self, request, vodeo_id):
        if vodeo_id:
            video = VideoInfo.objects.filter(id=vodeo_id)[0]
            video_url = video.url
            course = video.lesson.course
            # 记录用户学习课程
            usercourse_list = UserCourse.objects.filter(study_man=request.user, study_course=course)
            if not usercourse_list:
                user = UserCourse()
                user.study_man = request.user
                user.study_course = course
                user.save()
                course.study_num += 1
                course.save()

                usercourse_list = UserCourse.objects.filter(study_man=request.user)
                couse_list = [usercourse.study_man for usercourse in usercourse_list]
                org_list = set([course.org for course in couse_list])

                if course.org not in org_list:
                    course.org.love_num += 1
                    course.org.save()

            # 学过该课程的人还学过
            # 1.从中建表中获取到用户课程表对象
            usercourse_list = UserCourse.objects.filter(study_course=course)

            # 2.根据找到的用户学习课程，找到用户列表
            user_list = [usercourse.study_man for usercourse in usercourse_list]

            # 3.再根据找到的用户从学习的课程表中找到用户学习其它课程的整个对象
            usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

            # 4.从获取到的用户课程列表中拿到我们需要的其它课程,使用set集合去重
            course_list = set([usercourse.study_course for usercourse in usercourse_list])

            if course:
                return render(request, 'courses/course-play.html', {
                    'course': course,
                    'course_list': course_list,
                    'video_url': video_url,
                })


class CourseComment(View):
    """
    CourseComment 课程评论
    """
    def get(self, request, course_id):
        if course_id:
            course = CourseInfo.objects.filter(id=course_id)[0]
            all_comment = course.usercomment_set.all()[:10]
            # 学过该课程的人还学过
            # 1.从中建表中获取到用户课程表对象
            usercourse_list = UserCourse.objects.filter(study_course=course)

            # 2.根据找到的用户学习课程，找到用户列表
            user_list = [usercourse.study_man for usercourse in usercourse_list]

            # 3.再根据找到的用户从学习的课程表中找到用户学习其它课程的整个对象
            usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

            # 4.从获取到的用户课程列表中拿到我们需要的其它课程,使用set集合去重
            course_list = set([usercourse.study_course for usercourse in usercourse_list])

            return render(request, 'courses/course-comment.html', {
                'course': course,
                'course_list': course_list,
                'all_comment': all_comment,
            })


class CourseVideo(View):
    """
    CourseVideo 课程学习
    """
    @login_decorator
    def get(self, request, course_id):
        if course_id:
            course = CourseInfo.objects.filter(id=course_id)[0]

            # 记录用户学习课程
            usercourse_list = UserCourse.objects.filter(study_man=request.user, study_course=course)
            if not usercourse_list:
                user = UserCourse()
                user.study_man = request.user
                user.study_course = course
                user.save()
                course.study_num += 1
                course.save()

                usercourse_list = UserCourse.objects.filter(study_man=request.user)
                couse_list = [usercourse.study_man for usercourse in usercourse_list]
                org_list = set([course.org for course in couse_list])

                if course.org not in org_list:
                    course.org.love_num += 1
                    course.org.save()

            # 学过该课程的人还学过
            # 1.从中建表中获取到用户课程表对象
            usercourse_list = UserCourse.objects.filter(study_course=course)

            # 2.根据找到的用户学习课程，找到用户列表
            user_list = [usercourse.study_man for usercourse in usercourse_list]

            # 3.再根据找到的用户从学习的课程表中找到用户学习其它课程的整个对象
            usercourse_list = UserCourse.objects.filter(study_man__in=user_list).exclude(study_course=course)

            # 4.从获取到的用户课程列表中拿到我们需要的其它课程,使用set集合去重
            course_list = set([usercourse.study_course for usercourse in usercourse_list])

            if course:
                return render(request, 'courses/course-video.html', {
                    'course': course,
                    'course_list': course_list,
                })

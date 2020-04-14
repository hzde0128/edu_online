from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.generic import View

from .models import OrgInfo, CityInfo, TeacherInfo
from operations.models import UserLove


# Create your views here.
class OrgList(View):
    """
    org_list 机构列表展示
    """
    @staticmethod
    def get(request):
        all_orgs = OrgInfo.objects.all()
        all_citys = CityInfo.objects.all()
        sort_orgs = all_orgs.order_by('-love_num')[:3]

        # 全局搜索过滤,模糊搜索
        keyword = request.GET.get('keyword', '')
        if keyword:
            all_orgs = all_orgs.filter(Q(name__icontains=keyword)|Q(desc__icontains=keyword)|Q(detail__icontains=keyword))

        # 根据机构类型进行过滤
        category = request.GET.get('cat', '')
        if category:
            all_orgs = all_orgs.filter(org_category=category)

        # 根据城市进行过滤
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'course_num':
                pass
            else:
                all_orgs = all_orgs.order_by('-'+sort)

        # 分页
        page = request.GET.get('page')
        pa = Paginator(all_orgs, 2)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'orgs/org-list.html', {
            'all_orgs': all_orgs,
            'all_citys': all_citys,
            'sort_orgs': sort_orgs,
            'pages': pages,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'keyword': keyword,
        })


class OrgDetail(View):
    """
    org_detail 机构详情页
    用户点击机构详情页，点击数+1
    当用户登录时显示用户收藏状态信息
    @params org_id: 机构id 通过查询数据库找到对应的机构进行展示
    """
    @staticmethod
    def get(request, org_id):
        if org_id:
            org = OrgInfo.objects.filter(id=int(org_id))[0]

            # 动态修改机构点击数
            org.click_num += 1

            org.save()
            # 在返回页面数据的时候，需要返回收藏这个机构的收藏状态
            love_status = False
            if request.user.is_authenticated:
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
                if love:
                    love_status = True

            return render(request, 'orgs/org-detail-homepage.html', {
                'org': org,
                'detail_type': 'home',
                'love_status': love_status,
            })


class OrgDetailCourse(View):
    """
    org_detail_course 机构详情页-机构课程
    """
    def get(self, request, org_id):
        if org_id:
            org = OrgInfo.objects.filter(id=int(org_id))[0]
            love_status = False
            if request.user.is_authenticated:
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
                if love:
                    love_status = True

            return render(request, 'orgs/org-detail-course.html', {
                'org': org,
                'detail_type': 'course',
                'love_status': love_status,
            })


class OrgDetailDesc(View):
    """
    org_detail_desc 机构详情页-机构描述
    """
    def get(self, request, org_id):
        if org_id:
            org = OrgInfo.objects.filter(id=int(org_id))[0]
            love_status = False
            if request.user.is_authenticated:
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
                if love:
                    love_status = True

            return render(request, 'orgs/org-detail-desc.html', {
                'org': org,
                'detail_type': 'desc',
                'love_status': love_status,
            })


class OrgDetailTeacher(View):
    """
    org_detail_teacher 机构详情页-机构讲师
    """
    def get(self, request, org_id):
        if org_id:
            org = OrgInfo.objects.filter(id=int(org_id))[0]
            love_status = False
            if request.user.is_authenticated:
                love = UserLove.objects.filter(love_man=request.user, love_id=int(org_id), love_type=1, love_status=True)
                if love:
                    love_status = True

            return render(request, 'orgs/org-detail-teachers.html', {
                'org': org,
                'detail_type': 'teacher',
                'love_status': love_status,
            })


class TeacherList(View):
    """
    teacher_list 讲师列表
    """
    @staticmethod
    def get(request):
        all_teachers = TeacherInfo.objects.all()
        recommend = all_teachers.order_by('-love_num')[:2]

        # 全局搜索过滤,模糊搜索
        keyword = request.GET.get('keyword', '')
        if keyword:
            all_teachers = all_teachers.filter(Q(name__icontains=keyword))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            all_teachers = all_teachers.order_by('-' + sort)

        # 分页
        page = request.GET.get('page')
        pa = Paginator(all_teachers, 2)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'orgs/teachers-list.html', {
            'all_teachers': all_teachers,
            'pages': pages,
            'recommend': recommend,
            'sort': sort,
            'keyword': keyword,
        })


class TeacherDetail(View):
    """
    teacher_detail 讲师详情
    """
    def get(self, request, teacher_id):
        if teacher_id:
            teacher_list = TeacherInfo.objects.filter(id=teacher_id)
            if teacher_list:
                teacher = teacher_list[0]

            teacher.click_num += 1
            teacher.save()

            # 讲师排行
            recommend = TeacherInfo.objects.all().order_by('-click_num')[:3]

            return render(request, 'orgs/teacher-detail.html', {
                'teacher': teacher,
                'recommend': recommend,
            })

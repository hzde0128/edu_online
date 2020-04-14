from datetime import datetime

from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.backends import ModelBackend
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import UserRegisterForm, UserLoginForm, UserForgetForm, UserResetForm, UserAvatarForm, \
                   UpdateInfoForm, UserEmailForm, ResetEmailForm
from .models import UserProfile, EmailVerifyCode, BannerInfo
# 发送邮件
from utils.send_email import send_mail_code
from operations.models import UserLove, UserMessage
from courses.models import CourseInfo
from orgs.models import OrgInfo, TeacherInfo
from utils.decorators import login_decorator


# Create your views here.
class AuthBackend(ModelBackend):
    """
    AuthBackend 用户自定义登录认证
    用来同时支持用户名，邮箱，手机号码登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def handler_404(request, exception=404, template_name='handler_404.html'):
    """
    handler_404 自定义404错误
    只有在Debug == False的时候生效
    """
    return render(request, template_name)


def handler_500(request, exception=500, template_name='handler_500.html'):
    """
    handler_500 自定义500错误
    只有在Debug == False的时候生效
    """
    return render(request, template_name)


class IndexView(View):
    """
    IndexView 首页数据展示
    """
    @staticmethod
    def get(request):
        all_banners = BannerInfo.objects.all().order_by('-add_time')[:5]
        all_courses = CourseInfo.objects.filter(is_banner=False).order_by('-add_time')
        banner_course = CourseInfo.objects.filter(is_banner=True).order_by('-add_time')
        all_orgs = OrgInfo.objects.all().order_by('-add_time')

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'all_courses': all_courses,
            'banner_course': banner_course,
            'all_orgs': all_orgs,
        })


class UserRegister(View):
    """
    user_register 用户注册页面展示已经处理
    """
    @staticmethod
    def get(request):
        # 加载验证码
        user_register_form = UserRegisterForm()
        return render(request, 'users/register.html', {
            'user_register_form': user_register_form,
        })

    @staticmethod
    def post(request):
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']
            # 查找是否已经注册
            user_list = UserProfile.objects.filter(Q(username=email) | Q(email=email))
            if user_list:
                return render(request, 'users/register.html', {
                    'msg': '用户已经存在',
                })
            else:
                """
                默认未激活，需要点击邮箱链接进行激活
                """
                user = UserProfile(username=email, email=email)
                user.is_active = False
                user.set_password(password)
                user.save()
                """
                给用户发送激活邮件并发送欢迎注册消息
                """
                msg = UserMessage()
                msg.msg_content = '欢迎注册[在线教育网]，请遵守国家相关法律法规'
                msg.msg_user = user.id
                msg.save()
                send_mail_code(email, 1)
                return HttpResponse('请尽快前往您的邮箱激活，否则无法登录')
        else:
            return render(request, 'users/register.html', {
                'user_register_form': user_register_form,
            })


class UserLogin(View):
    """
    UserLogin 用户登录页面和处理
    """
    @staticmethod
    def get(request):
        return render(request, 'users/login.html')

    @staticmethod
    def post(request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            username = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                """"
                仅允许激活用户允许进行登录
                """
                if user.is_active:
                    login(request, user)
                    # 登录消息
                    msg = UserMessage()
                    msg.msg_user = user.id
                    msg.msg_content = '欢迎登录'
                    msg.save()
                    url = request.COOKIES.get('url', '/')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
                else:
                    return render(request, 'users/login.html', {
                        'msg': '该账户未激活，请先去邮箱激活。',
                    })
            else:
                return render(request, 'users/login.html', {
                    'msg': '用户名或密码错误',
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form,
            })


class UserForget(View):
    """
    user_forget 忘记密码页面展示以及处理
    """
    def get(self, request):
        user_forget_form = UserForgetForm()
        return render(request, 'users/forgetpwd.html', {
            'user_forget_form': user_forget_form,
        })

    def post(self, request):
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            # 查询邮箱是否存在
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_mail_code(email, 2)
                return HttpResponse('请尽快去您的邮箱去重置您的密码')
            else:
                return render(request, 'users/forgetpwd.html', {
                    'msg': '用户不存在',
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'user_forget_form': user_forget_form,
            })


class UserReset(View):
    """
    UserReset 重置用户密码页面以及处理
    """
    @login_decorator
    def get(self, request, code):
        if code:
            return render(request, 'users/password_reset.html', {
                'code': code
            })

    @login_decorator
    def post(self, request, code):
        if code:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password2 = user_reset_form.cleaned_data['password2']
                if password == password2:
                    email_ver_list = EmailVerifyCode.objects.filter(code=code)
                    if email_ver_list:
                        email_ver = email_ver_list[0]
                        email = email_ver.email
                        user_list = UserProfile.objects.filter(email=email)
                        if user_list:
                            user = user_list[0]
                            user.set_password(password)
                            user.save()
                            return redirect(reverse('users:user_login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'code': code,
                        'msg': '两次密码不一致',
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'code': code,
                    'user_reset_form': user_reset_form,
                })


class UserInfo(View):
    """
    user_info 用户中心页面显示
    @params: request: 通过request获取当前用户信息展示
    """
    @login_decorator
    def get(self, request):
        return render(request, 'users/usercenter-info.html')


class UserInfoCourse(View):
    @login_decorator
    def get(self, request):
        usercourse_list = request.user.usercourse_set.all()
        my_courses = [usercourse.study_course for usercourse in usercourse_list]
        return render(request, 'users/usercenter-mycourse.html', {
            'my_courses': my_courses,
        })


class UserInfoFavOrg(View):
    @login_decorator
    def get(self, request):
        userlove_orgs = UserLove.objects.filter(love_man=request.user, love_type=1, love_status=True)
        org_ids = [userlove.love_id for userlove in userlove_orgs]
        orgs = OrgInfo.objects.filter(id__in=org_ids)
        return render(request, 'users/usercenter-fav-org.html', {
            'orgs': orgs,
        })


class UserInfoFavCourse(View):
    @login_decorator
    def get(self, request):
        userlove_courses = UserLove.objects.filter(love_man=request.user, love_type=2, love_status=True)
        courses_ids = [userlove.love_id for userlove in userlove_courses]
        courses = CourseInfo.objects.filter(id__in=courses_ids)
        return render(request, 'users/usercenter-fav-course.html', {
            'courses': courses,
        })


class UserInfoFavTeacher(View):
    @login_decorator
    def get(self, request):
        userlove_teacher = UserLove.objects.filter(love_man=request.user, love_type=3, love_status=True)
        teacher_ids = [userlove.love_id for userlove in userlove_teacher]
        teachers = TeacherInfo.objects.filter(id__in=teacher_ids)
        return render(request, 'users/usercenter-fav-teacher.html', {
            'teachers': teachers,
        })


class UserInfoMessage(View):
    """
    显示用户消息列表
    按照时间倒序排序
    增加分页显示功能， 每页显示5条
    @params:request 获取当前用户信息，从当前用户找到对应的消息列表
    @return: 返回消息列表给前端展示
    """
    @login_decorator
    def get(self, request):
        msg_list = UserMessage.objects.filter(msg_user=request.user.id).order_by('-add_time')

        page = request.GET.get('page')
        pa = Paginator(msg_list, 5)
        try:
            pages = pa.page(page)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)

        return render(request, 'users/usercenter-message.html', {
            'msg_list': msg_list,
            'pages': pages,
        })


class UserInfoMessageRead(View):
    @login_decorator
    def get(self, request):
        msg_id = request.GET.get('msg_id', '')
        if msg_id:
            msg = UserMessage.objects.filter(id=int(msg_id))[0]
            msg.msg_status = True
            msg.save()
            return JsonResponse({'status': 'ok', 'msg': '已经阅读'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '阅读失败'})


class AvatarUpload(View):
    """
    AvatarUpload 上传用户头像
    """
    @staticmethod
    def post(request):
        user_avatar_form = UserAvatarForm(request.POST, request.FILES, instance=request.user)
        if user_avatar_form.is_valid():
            user_avatar_form.save(commit=True)
            return JsonResponse({'status': 'ok', 'msg': '上传成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '上传失败'})


class UpdateInfo(View):
    """
    UpdateInfo 修改用户基础信息
    """
    @staticmethod
    def post(request):
        update_info_form = UpdateInfoForm(request.POST, instance=request.user)
        if update_info_form.is_valid():
            update_info_form.save(commit=True)
            return JsonResponse({'status': 'ok', 'msg': '修改成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '修改失败'})


class UserLogout(View):
    """
    UserLogout 登出
    """
    @staticmethod
    def get(request):
        logout(request)
        return redirect(reverse('index'))


class UserActive(View):
    """
    UserActive 用户激活
    从url中获取code,并对code记录进行判断超过5分钟设置未失效
    @prarms: request:
    @prarms: code
    """
    @staticmethod
    def get(request, code):
        if code:
            email_ver = EmailVerifyCode.objects.get(code=code)
            if email_ver:
                now = timezone.now()
                if (now - email_ver.add_time).seconds > 300:
                    return HttpResponse('链接已经失效，请重新获取')
                else:
                    email = email_ver.email
                    user = UserProfile.objects.get(username=email)
                    if user:
                        user.is_active = True
                        user.save()
                        return redirect(reverse("users:user_login"))
                    else:
                        return redirect(reverse('users:user_register'))
            else:
                return redirect(reverse('users:user_register'))
        else:
            return redirect(reverse('users:user_register'))


class UpdateEmail(View):
    """
    当用户修改邮箱，点击获取验证码的时候，会通过这个函数处理，发送邮箱验证码
    :param request:http请求对象
    :return:返回json数据，在模版页面当中处理
    """
    @staticmethod
    def post(request):
        user_email_form = UserEmailForm(request.POST)
        if user_email_form.is_valid():
            email = user_email_form.cleaned_data['email']
            # 判断新邮箱是否已经存在数据库中
            user_list = UserProfile.objects.filter(Q(email=email)|Q(username=email))
            if user_list:
                return JsonResponse({'status': 'fail', 'msg': '该邮箱已经被绑定'})
            else:
                # 增加发送邮箱时间限制
                email_ver_list = EmailVerifyCode.objects.filter(email=email, send_type=3)
                if email_ver_list:
                    # 拿到更换邮箱的验证码最近的记录
                    email_ver = email_ver_list.order_by('-add_time')[0]
                    # 判断当前时间跟上次发送邮件的时间差
                    now = timezone.now()
                    if (now - email_ver.add_time).seconds > 300:
                        # 如果重新发送了新的验证码，那么之前发送的验证码失效
                        # 给用户发邮件
                        send_mail_code(email, 3)
                        email_ver.delete()
                        return JsonResponse({'status': 'ok', 'msg': '验证码已发送到您的邮箱，请前往邮箱获取'})
                    else:
                        return JsonResponse({'status': 'fail', 'msg': '请不要重复发送，5分钟后重试'})
                else:
                    send_mail_code(email, 3)
                    return JsonResponse({'status': 'ok', 'msg': '验证码已发送到您的邮箱，请前往邮箱获取'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '您的邮箱格式不正确'})


class ResetEmail(View):
    """
    reset_email 重置用户密码处理
    根据页面输入的用户验证码与数据库中的数据进行校验
    并设置验证码有效期为5分钟，过期提示用户重新点获取验证码获取
    """
    @staticmethod
    def post(request):
        reset_email_form = ResetEmailForm(request.POST)
        if reset_email_form.is_valid():
            email = reset_email_form.cleaned_data['email']
            code = reset_email_form.cleaned_data['code']
            email_ver_list = EmailVerifyCode.objects.filter(email=email, code=code)
            if email_ver_list:
                # 验证通过，更换用户邮箱
                email_ver = email_ver_list[0]
                # 验证码过期时间,5分钟有效
                print(datetime.now())
                print(email_ver.add_time)
                now = timezone.now()
                if (now - email_ver.add_time).seconds < 300:
                    request.user.email = email
                    request.user.username = email
                    request.user.save()
                    return JsonResponse({'status': 'ok', 'msg': '邮箱修改成功'})
                else:
                    return JsonResponse({'status': 'fail', 'msg': '验证码已过去，请重新发送验证码'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '邮箱或验证码有误'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '邮箱或者验证码不合法'})


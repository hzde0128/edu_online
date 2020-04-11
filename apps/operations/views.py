from django.shortcuts import render
from .forms import UserAskForm, UserCommentForm
from django.http import JsonResponse
from .models import UserLove, UserComment
from orgs.models import OrgInfo, TeacherInfo
from courses.models import CourseInfo
from utils.decorators import login_decorator


# Create your views here.
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        # name = user_ask_form.cleaned_data['name']
        # phone = user_ask_form.cleaned_data['phone']
        # course = user_ask_form.cleaned_data['course']
        user_ask_form.save(commit=True)
        return JsonResponse({"status": 'OK', 'msg': '咨询成功'})
    else:
        return JsonResponse({"status": 'FAIL', 'msg': '咨询失败'})


@login_decorator
def user_love(request):
    love_id = request.GET.get('love_id', '')
    love_type = request.GET.get('love_type', '')
    print(love_id, love_type)
    if love_id and love_type:
        # 根据传过来的收藏类型，判断是什么对象，根据收藏ID，判断是哪个对象
        obj = None
        if int(love_type) == 1:
            obj = OrgInfo.objects.filter(id=int(love_id))[0]
        if int(love_type) == 2:
            obj = CourseInfo.objects.filter(id=int(love_id))[0]
        if int(love_type) == 3:
            obj = TeacherInfo.objects.filter(id=int(love_id))[0]

        love = UserLove.objects.filter(love_id=love_id, love_type=love_type, love_man=request.user)
        if love:
            # 判断之前是否已经收藏，有则取消收藏，否则收藏
            if love[0].love_status:
                love[0].love_status = False
                love[0].save()
                obj.love_num -= 1
                obj.save()
                return JsonResponse({'status': 'ok', 'msg': '收藏'})
            else:
                love[0].love_status = True
                love[0].save()
                obj.love_num += 1
                obj.save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            user = UserLove()
            user.love_man = request.user
            user.love_id = love_id
            user.love_type = int(love_type)
            user.save()
            obj.love_num += 1
            obj.save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '收藏失败'})


@login_decorator
def user_delete_love(request):
    love_id = request.GET.get('love_id', '')
    love_type = request.GET.get('love_type', '')
    if love_id and love_type:
        love = UserLove.objects.filter(love_id=int(love_id), love_type=int(love_type), love_man=request.user, love_status=True)
        if love:
            love[0].love_status = False
            love[0].save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '取消收藏失败'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '取消收藏失败'})


@login_decorator
def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        course = user_comment_form.cleaned_data['course']
        content = user_comment_form.cleaned_data['content']
        a = UserComment()
        a.comment_man = request.user
        a.content = content
        a.comment_course_id = course
        a.save()
        return JsonResponse({'status': 'ok', 'msg': '评论成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '评论失败'})


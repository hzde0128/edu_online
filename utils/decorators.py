from django.shortcuts import redirect, reverse
from django.http import JsonResponse


def login_decorator(func):
    """
    自定义的登录装饰器
    如果登录，继续
    如果未登录，跳转到登录页面
    """
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            # 判断请求是否为ajax
            if request.is_ajax():
                return JsonResponse({'status': 'nologin'})

            # 拿到目前访问的完整url，不只是路径部分
            url = request.get_full_path()
            ret = redirect(reverse('users:user_login'))
            ret.set_cookie('url', url)
            return ret
    return inner


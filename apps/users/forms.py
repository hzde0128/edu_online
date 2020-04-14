from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile, EmailVerifyCode


class UserRegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少6位',
        'max_length': '密码不能超过20位',
    })
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class UserLoginForm(forms.Form):
    """
    username 可以是用户名，邮箱和手机号
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少6位',
        'max_length': '密码不能超过20位',
    })


class UserForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class UserResetForm(forms.Form):
    password = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少6位',
        'max_length': '密码不能超过20位',
    })
    password2 = forms.CharField(required=True, min_length=6, max_length=20, error_messages={
        'required': '密码必须填写',
        'min_length': '密码至少6位',
        'max_length': '密码不能超过20位',
    })


class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'address', 'phone', 'birthday']


class UserEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


class ResetEmailForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyCode
        fields = ['email', 'code']

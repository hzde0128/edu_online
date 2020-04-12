from django import forms
from .models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    """
    UserAskForm 用户咨询表单
    接收三个参数 name course phone
    """
    # ModelForm Model和Form的结合体
    class Meta:
        model = UserAsk
        fields = ['name', 'course', 'phone']
        # exclude = ['add_time']
        # 如果用到所有的字段 fields = '__all__'

    def clean_phone(self):
        """
        通过正则表达式验证提交过来的手机号码是否合法
        """
        phone = self.cleaned_data['phone']
        com = re.compile('^1[34578]\d{9}$')
        if com.match(phone):
            return phone
        else:
            # 手机号码验证失败
            raise forms.ValidationError('手机号码不合法')

    # def clean_course(self):


class UserCommentForm(forms.Form):
    """
    UserCommentForm 用户评论表单
    """
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=5, max_length=300)

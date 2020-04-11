from django import forms
from .models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    # ModelForm Model和Form的结合体
    class Meta:
        model = UserAsk
        fields = ['name', 'course', 'phone']
        # exclude = ['add_time']
        # 如果用到所有的字段 fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        com = re.compile('^1[34578]\d{9}$')
        if com.match(phone):
            return phone
        else:
            # 手机号码验证失败
            raise forms.ValidationError('手机号码不合法')

    # def clean_course(self):


class UserCommentForm(forms.Form):
    course = forms.IntegerField(required=True)
    content = forms.CharField(required=True, min_length=5, max_length=300)

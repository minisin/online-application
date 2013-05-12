# -*- coding: utf-8 -*-

from django import forms
from app.models import People
from django.core.exceptions import ValidationError
from app.functions import id_number_validator

class PeopleNoPasswordForm(forms.ModelForm):
    gender = forms.ChoiceField(widget=forms.RadioSelect, 
                               choices=People.gender_choices, 
                               label=u'性别 *')
    hometown_prov = forms.CharField(widget=forms.Select)
    hometown_city = forms.CharField(widget=forms.Select)
    residence_prov = forms.CharField(widget=forms.Select)
    residence_city = forms.CharField(widget=forms.Select)
    avator = forms.CharField() #widget=forms.HiddenInput
    # 修改自己信息的时候不需要验证密码
    query_password = forms.CharField(required=False)

    def clean_hometown_prov(self):
        if self.cleaned_data.get('hometown_prov').strip() == u'--':
            msg = u'请选择省份'
            self._errors['hometown_prov'] = self.error_class([msg])
            raise ValidationError(msg)
        return self.cleaned_data.get('hometown_prov')

    def clean_residence_prov(self):
        if self.cleaned_data.get('residence_prov').strip() == u'--':
            errmsg = u'请选择省份'
            self._errors['residence_prov'] = self.error_class([errmsg])
            raise ValidationError(errmsg)
        return self.cleaned_data.get('residence_prov')

    def clean_first_edu_end_month(self):
        start_date = "%s%s" % (self.cleaned_data.get('first_edu_start_year'), 
                             self.cleaned_data.get('first_edu_start_month'))
        end_date = "%s%s" % (self.cleaned_data.get('first_edu_end_year'), 
                             self.cleaned_data.get('first_edu_end_month'))
        if cmp(end_date, start_date) < 0:
            errmsg = u'结束时间不能早于开始时间'
            self._errors['first_edu_end_year'] = self.error_class([errmsg])
        return self.cleaned_data.get('first_edu_end_month')

    def clean_high_edu_edu_month(self):
        start_date = "%s%s" % (self.cleaned_data.get('high_edu_start_year'), 
                             self.cleaned_data.get('high_edu_start_month'))
        end_date = "%s%s" % (self.cleaned_data.get('high_edu_edu_year'), 
                             self.cleaned_data.get('high_edu_edu_month'))
        if cmp(end_date, start_date) < 0:
            errmsg = u'结束时间不能早于开始时间'
            self._errors['high_edu_edu_year'] = self.error_class([errmsg])
        return self.cleaned_data.get('high_edu_edu_month')

    def clean_other_edu_edu_month(self):
        start_date = "%s%s" % (self.cleaned_data.get('other_edu_start_year'), 
                             self.cleaned_data.get('other_edu_start_month'))
        end_date = "%s%s" % (self.cleaned_data.get('other_edu_edu_year'), 
                             self.cleaned_data.get('other_edu_edu_month'))
        if cmp(end_date, start_date) < 0:
            errmsg = u'结束时间不能早于开始时间'
            self._errors['other_edu_edu_year'] = self.error_class([errmsg])
        return self.cleaned_data.get('other_edu_edu_month')

    class Meta:
        model = People


class PeopleForm(PeopleNoPasswordForm):
    query_password = forms.CharField(widget=forms.PasswordInput)
    query_password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_query_password2(self):
        pwd1 = self.cleaned_data.get('query_password')
        pwd2 = self.cleaned_data.get('query_password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            errmsg = u'两次输入的密码不一致'
            self._errors['query_password2'] = self.error_class([errmsg])
            raise ValidationError(errmsg)
        return pwd2

    def clean(self):
        if People.objects.filter(id_number=self.cleaned_data.get('id_number'), 
                                 name=self.cleaned_data.get('name')):
            self._errors['__all__'] = self.error_class(['此姓名和身份证号已经填写过申请'])
        return self.cleaned_data


class LoginForm(forms.Form):
    id_number = forms.CharField(validators=[id_number_validator])
    password = forms.CharField(widget=forms.PasswordInput)
    

class FindpwdForm(forms.Form):
    id_number = forms.CharField(validators=[id_number_validator])
    email = forms.EmailField(error_messages={'invalid': '邮件格式不正确'})


class ChangepwdForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_confirm_password(self):
        pwd1 = self.cleaned_data.get('new_password')
        pwd2 = self.cleaned_data.get('confirm_password')
        if pwd1 and pwd2 and pwd1 != pwd2:
            errmsg = u'两次输入的密码不一致'
            self._errors['confirm_password'] = self.error_class([errmsg])
            raise ValidationError(errmsg)
        return pwd2

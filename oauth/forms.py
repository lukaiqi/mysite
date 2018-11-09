from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from oauth.models import OAuth_ex


class BindEmail(forms.Form):
    """bind the openid to email"""
    qq_openid = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'qq_openid'}))
    qq_nickname = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'qq_nickname'}))
    email = forms.EmailField(label='注册邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请输入您注册用的邮箱'}))
    password = forms.CharField(label='登录密码',
                               min_length=6,
                               max_length=16,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': '若尚未注册过，该密码则作为用户密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmail, self).__init__(*args, **kwargs)

    # 验证邮箱
    def clean_email(self):
        # qq_openid = self.cleaned_data.get('qq_openid')
        email = self.cleaned_data.get('email')
        users = User.objects.filter(email=email)

        if users:
            # 判断是否被绑定了
            if OAuth_ex.objects.filter(user=users[0]):
                raise forms.ValidationError('该邮箱已经被绑定了')
        return email  # 返回邮箱

    # 验证密码
    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        users = User.objects.filter(email=email)
        if users:
            # 若用户存在，判断密码是否正确
            user = auth.authenticate(username=users[0], password=password)
            if user is None:
                raise forms.ValidationError('密码不正确')
        return password  # 返回密码

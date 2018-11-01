from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱',
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': '请输入用户名'
                                                   })
                                        )
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'
                                                                 })
                               )

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control', 'placeholder': '请输入3-30位用户名'
                                   })
                               )
    phone = forms.CharField(label='手机号',
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control', 'placeholder': '请输入11位手机号'
                                })
                            )
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(
                                 attrs={
                                     'class': 'form-control', 'placeholder': '请输入邮箱'
                                 })
                             )
    verification_code = forms.CharField(label='验证码',
                                        max_length=6,
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '点击"发送验证码"发送到手机'
                                                   })
                                        )
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control', 'placeholder': '再输入一次密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称',
                                   max_length=20,
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control', 'placeholder': '请输入新的昵称'
                                       })
                                   )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNicknameForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='修改邮箱',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请输入新的邮箱'
                                        })
                             )
    verification_code = forms.CharField(label='验证码',
                                        max_length=4,
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '点击"发送验证码"发送到邮箱'
                                                   })
                                        )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangeEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 判断验证码
        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class ChangePhoneForm(forms.Form):
    phone = forms.CharField(label='新的手机号',
                            max_length=11,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请输入新的手机号'
                                        })
                             )
    verification_code = forms.CharField(label='验证码',
                                        max_length=4,
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '点击"发送验证码"发送到手机'
                                                   })
                                        )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ChangePhoneForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')
        # 判断验证码
        code = self.request.session.get('change_phone_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone_profile__phone=phone).exists():
            raise forms.ValidationError('手机号已被绑定')
        return phone


    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


class BindPhoneForm(forms.Form):
    phone = forms.CharField(label='手机号',
                            max_length=20,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control', 'placeholder': '请输入手机号'
                                })
                            )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(BindPhoneForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone == '':
            raise forms.ValidationError('手机号不能为空')
        return phone


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧密码',
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'class': 'form-control', 'placeholder': '请输入旧密码'
                                       })
                                   )
    new_password = forms.CharField(label='新密码',
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'class': 'form-control', 'placeholder': '请输入新的密码'
                                       })
                                   )
    renew_password = forms.CharField(label='确认新密码',
                                     widget=forms.PasswordInput(
                                         attrs={
                                             'class': 'form-control', 'placeholder': '请再次输入新得密码'
                                         })
                                     )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新得密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        renew_password = self.cleaned_data.get('renew_password', '')
        if new_password != renew_password or new_password == '':
            raise forms.ValidationError('两次输入密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码不正确')
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '请输入绑定过的邮箱'
                                        })
                             )
    verification_code = forms.CharField(label='验证码',
                                        max_length=6,
                                        required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '点击"发送验证码"发送到邮箱'
                                                   })
                                        )

    new_password = forms.CharField(label='新密码',
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'class': 'form-control', 'placeholder': '请输入新的密码'
                                       })
                                   )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        # 判断验证码
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code

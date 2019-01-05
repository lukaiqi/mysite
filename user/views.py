import json
import os
import string
import random
import time
import urllib
import uuid
from PIL import Image
from django.shortcuts import render, redirect
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegForm, ChangeNicknameForm, \
    ChangeEmailForm, ChangePasswordForm, ForgotPasswordForm, \
    BindPhoneForm, ChangePhoneForm
from .models import Profile, Phone_Profile


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            phone = reg_form.cleaned_data['phone']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            # 保存电话
            phone_profile, created = Phone_Profile.objects.get_or_create(user=request.user)
            phone_profile.phone = phone
            phone_profile.save()
            return redirect(request.GET.get('from', reverse('login')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def change_email(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['change_email_code']
            return redirect(redirect_to)
    else:
        form = ChangeEmailForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改邮箱'
    context['form_title'] = '修改邮箱'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'user/change_email.html', context)


def bind_phone(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = BindPhoneForm(request.POST, user=request.user)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            phone_profile, created = Phone_Profile.objects.get_or_create(user=request.user)
            phone_profile.phone = phone
            phone_profile.save()
            return redirect(redirect_to)
    else:
        form = BindPhoneForm()
    context = {}
    context['form'] = form
    context['page_title'] = '绑定手机号'
    context['form_title'] = '绑定手机号'
    context['submit_text'] = '绑定'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def change_phone(request):
    redirect_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = ChangePhoneForm(request.POST, request=request)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            phone_profile, created = Phone_Profile.objects.get_or_create(user=request.user)
            phone_profile.phone = phone
            phone_profile.save()
            return redirect(redirect_to)
    else:
        form = ChangePhoneForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改手机号'
    context['form_title'] = '修改手机号'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/change_phone.html', context)


def send_msg_verification_code(request):
    phone = request.GET.get('phone', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if phone != '':
        # 生成验证码
        code = ''.join(random.sample(string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
        host = 'http://dingxin.market.alicloudapi.com'
        path = '/dx/sendSms'
        method = 'POST'
        appcode = settings.APP_CODE
        querys = 'mobile=' + phone + '&param=code%3A' + code + '&tpl_id=TP1712202'
        url = host + path + '?' + querys

        request = urllib.request.Request(url)
        request.method = method
        request.add_header('Authorization', 'APPCODE ' + appcode)
        response = urllib.request.urlopen(request)
        content = response.read()
        if (content):
            print(content)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def send_email_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
        # 发送邮件
        send_mail(
            '邮箱验证',
            '验证码 %s' % code,
            '1263041461@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
        return redirect(reverse('home'))
    else:
        form = ChangePasswordForm()
    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)


def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)


def user_avatar(request):
    if request.user.is_authenticated:
        data = {}
        data['user'] = request.user
        return render(request, 'user/avatar.html', data)
    else:
        return render(request, 'error.html')


@csrf_exempt
def user_avatar_upload(request):
    if request.user.is_authenticated:
        data = {}
        avatar_file = request.FILES['avatar_file']
        temp_folder = os.path.join('media', 'temp')
        if not os.path.isdir(temp_folder):
            os.makedirs(temp_folder)
        temp_filename = uuid.uuid1().hex + os.path.splitext(avatar_file.name)[-1]
        temp_path = os.path.join(temp_folder, temp_filename)
        # 保存上传的文件
        with open(temp_path, 'wb') as f:
            for chunk in avatar_file.chunks():
                f.write(chunk)
        # 裁剪图片
        top = int(float(request.POST['avatar_y']))
        buttom = top + int(float(request.POST['avatar_height']))
        left = int(float(request.POST['avatar_x']))
        right = left + int(float(request.POST['avatar_width']))
        im = Image.open(temp_path)
        chanel = len(im.split())
        # 裁剪图片
        crop_im = im.convert("RGBA").crop((left, top, right, buttom)).resize((64, 64), Image.ANTIALIAS)
        if chanel == 4:
            # 设置背景颜色为白色
            out = crop_im
        else:
            out = crop_im.convert('RGB')
        out.paste(crop_im, (0, 0, 64, 64), crop_im)

        # 保存图片
        out.save(temp_path)

        # 保存记录
        avatar = request.user.set_avatar_url(temp_path)
        os.remove(temp_path)
        #
        data['success'] = True
        # data['avatar_url'] = avatar.avatar.name
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'error.html')

import string
import random
import time
import os
import urllib, urllib.request, sys
from os import listdir
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.encoding import escape_uri_path
from .forms import LoginForm, RegForm, ChangeNicknameForm, \
    ChangeEmailForm, ChangePasswordForm, ForgotPasswordForm, \
    BindPhoneForm, ChangePhoneForm
from .models import Profile, SendMail, Phone_Profile, Info, \
    Statistics
from visit.models import Statistics


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
            # 获取ip地址
            ipaddr = get_ip(request).getvalue()
            str = bytes.decode(ipaddr)
            IP = str.split(':')[1].split('}')[0]
            # 发送邮件
            SendMail.send_mail_reg(username, IP, phone)
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
    Statistics.count(request)
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
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
        host = 'http://dingxin.market.alicloudapi.com'
        path = '/dx/sendSms'
        method = 'POST'
        appcode = '6b5974d1336f415ca1901fd6ef6fe95b'
        querys = 'mobile=' + phone + '&param=code%3A' + code + '&tpl_id=TP1712202'
        bodys = {}
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
        if now - send_code_time < 30:
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


def get_ip(request):
    data = {}
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
    data['client_ip'] = client_ip
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


def upload_file(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("未选择上传文件")
        destination = open(os.path.join("/home/mysite/files", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return render(request, 'home.html')


def upload(request):
    return render(request, 'user/file_upload.html')


def file_list(request):
    if request.user.is_superuser:
        # file_path = 'G:\\mysite_env\\mysite\\templates\\'
        file_path = '/home/mysite/files/'
        file_name_list = listdir(file_path)
        context = {}
        context['file_name_list'] = file_name_list
        return render(request, 'user/files.html', context)
    else:
        return render(request, 'error.html')


def file_download(request):
    name = request.GET.get('filename')
    # base_path = 'G:\\mysite_env\\mysite\\templates\\'
    base_path = '/home/mysite/files/'
    file_path = base_path + name
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(name))
    return response


def file_delete(request):
    name = request.GET.get('filename')
    # base_path = 'G:\\mysite_env\\mysite\\templates\\'
    base_path = '/home/mysite/files/'
    file_path = base_path + name
    os.remove(file_path)
    return render(request, 'user/file_del.html')


def info(request):
    Statistics.count(request)
    info = Info.objects.all()
    content = list(info)[0]
    text = content.text
    time = content.send_time
    context = {}
    context['time'] = time
    context['text'] = text
    return render(request, 'user/info.html', context)




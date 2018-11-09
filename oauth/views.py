import time
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.urls import reverse  # url逆向解析
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.conf import settings
from oauth.oauth_client import OAuth_QQ
from oauth.models import OAuth_ex
from oauth.forms import BindEmail
from user.models import Profile


def qq_login(request):
    oauth_qq = OAuth_QQ(settings.QQ_APP_ID, settings.QQ_APP_KEY, settings.QQ_RECALL_URL)
    # 获取 得到Authorization Code的地址
    url = oauth_qq.get_auth_url()
    # 重定向到授权页面
    return HttpResponseRedirect(url)


def qq_check(request):
    """登录之后，会跳转到这里。需要判断code和state"""
    request_code = request.GET.get('code')
    oauth_qq = OAuth_QQ(settings.QQ_APP_ID, settings.QQ_APP_KEY, settings.QQ_RECALL_URL)

    # 获取access_token
    access_token = oauth_qq.get_access_token(request_code)
    time.sleep(0.05)  # 稍微休息一下，避免发送urlopen的10060错误
    open_id = oauth_qq.get_open_id()

    # 检查open_id是否存在
    qqs = OAuth_ex.objects.filter(qq_openid=open_id)
    if qqs:
        # 存在则获取对应的用户，并登录
        user = qqs[0].user

        # 设置backend，绕开authenticate验证
        setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')

        login(request, user)
        return HttpResponseRedirect('/')
    else:
        # 不存在，则跳转到绑定邮箱页面
        infos = oauth_qq.get_qq_info()  # 获取用户信息
        url = '%s?open_id=%s&nickname=%s' % (reverse('bind_email'), open_id, infos['nickname'])
        return HttpResponseRedirect(url)


def bind_email(request):
    open_id = request.GET.get('open_id')
    nickname = request.GET.get('nickname')
    data = {}
    data['page_title'] = '绑定'
    data['form_title'] = '绑定用户'
    data['submit_text'] = '确定'
    data['form_tip'] = 'Hi, <span class="label label-info">' \
                       '<img src="/static/images/qq_logo.png">%s</span>！' \
                       '您已登录。请绑定用户，完成QQ登录' % nickname

    if request.method == 'POST':
        # 表单提交
        form = BindEmail(request.POST, request=request)
        # 验证是否合法
        if form.is_valid():
            qq_openid = form.cleaned_data['qq_openid']
            qq_nickname = form.cleaned_data['qq_nickname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            users = User.objects.filter(email=email)
            if users:
                username = users[0]
                # 用户存在，则直接绑定
                profile, created = Profile.objects.get_or_create(user=username)
                profile.nickname = qq_nickname
                profile.save()
                # 绑定用户
                oauth_ex = OAuth_ex(user=username, qq_openid=qq_openid)
                oauth_ex.save()
                # 登录用户
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
            else:
                # 用户不存在，则注册
                username = qq_nickname  # 使用QQ昵称作为用户名
                user = User.objects.create_user(username, email, password)
                user.save()
                # 绑定用户
                oauth_ex = OAuth_ex(user=user, qq_openid=qq_openid)
                oauth_ex.save()
                # 登录用户
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)

            return render(request, 'home.html')
    else:
        # 正常加载
        form = BindEmail(initial={
            'qq_openid': open_id,
            'qq_nickname': nickname,
        })
    data['form'] = form
    return render(request, 'bind_email.html', data)

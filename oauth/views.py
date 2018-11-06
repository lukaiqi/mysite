from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.urls import reverse  # url逆向解析
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
from oauth.oauth_client import OAuth_QQ
from oauth.models import OAuth_ex
from oauth.forms import BindEmail
import time


# http://yshblog.com/oauth/qq_login
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

    data['form_title'] = '绑定用户'
    data['submit_name'] = '确定'
    data['form_tip'] = 'Hi, <span class="label label-info">' \
                       '<img src="/static/img/connect/logo_qq.png">%s</span>！' \
                       '您已登录。请绑定用户，完成QQ登录' % nickname

    if request.method == 'POST':
        # 表单提交
        form = BindEmail(request.POST)

        # 验证是否合法
        if form.is_valid():
            # 判断邮箱是否注册了
            qq_openid = form.cleaned_data['qq_openid']
            qq_nickname = form.cleaned_data['qq_nickname']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd']

            users = User.objects.filter(email=email)
            if users:
                # 用户存在，则直接绑定
                user = users[0]
                if not user.first_name:
                    user.first_name = qq_nickname  # 更新昵称
                    user.save()
                data['message'] = u'绑定账号成功，绑定到%s”' % email
            else:
                # 用户不存在，则注册，并发送激活邮件
                user = User(username=email, email=email)
                user.first_name = qq_nickname  # 使用QQ昵称作为昵称
                user.set_password(pwd)
                user.is_active = False
                user.save()
                data['message'] = '绑定账号成功，绑定到%s'

            # 绑定用户并
            oauth_ex = OAuth_ex(user=user, qq_openid=qq_openid)
            oauth_ex.save()

            # 登录用户
            user = authenticate(username=email, password=pwd)
            if user is not None:
                login(request, user)

            # 页面提示
            data['goto_url'] = '/'
            data['goto_time'] = 3000
            data['goto_page'] = True

            return render_to_response('message.html', data)
    else:
        # 正常加载
        form = BindEmail(initial={
            'qq_openid': open_id,
            'qq_nickname': nickname,
        })
    data['form'] = form
    return render(request, 'form.html', data)

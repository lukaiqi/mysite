import threading
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname, self.user.username)


class SendMail(threading.Thread):

    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.text,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently
        )

    def send_mail_to_admin(username, ipaddr,phone):
        subject = '新用户注册通知'
        email = 'lkq18328816819@gmail.com'
        text = '新用户: ' + username + ' 注册成功!' + 'ip地址为:' + ipaddr + '!' + '手机号为:' + phone
        send_mail = SendMail(subject, text, email)
        send_mail.start()


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username

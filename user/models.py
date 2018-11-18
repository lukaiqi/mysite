import threading
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20)

    class Meta:
        verbose_name = '昵称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname, self.user.username)


class Phone_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='电话')
    phone = models.CharField(max_length=11)

    class Meta:
        verbose_name = '电话'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Phone:%s >' % (self.phone)


class Info(models.Model):
    user = models.ForeignKey(User, related_name="info", on_delete=models.CASCADE)
    send_time = models.DateTimeField(auto_now=True)
    text = RichTextUploadingField()

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Text:%s >' % (self.text)


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

    def send_mail_reg(username, ipaddr, phone):
        subject = '新用户注册通知'
        email = 'mengluowusheng@gmail.com'
        text = '新用户: ' + username + ' 注册成功!' + 'ip地址为:' + ipaddr + '!' + '手机号为:' + phone
        send_mail = SendMail(subject, text, email)
        send_mail.start()

    def send_mail_qqbind(username, ipaddr, nickname):
        subject = '新用户注册通知'
        email = 'mengluowusheng@gmail.com'
        text = '用户: ' + username + ' 绑定qq号成功!' + 'ip地址为:' + ipaddr + '!' + 'qq昵称为:' + nickname
        send_mail = SendMail(subject, text, email)
        send_mail.start()

    def send_mail_qqreg(username, ipaddr, nickname):
        subject = '新用户注册通知'
        email = 'mengluowusheng@gmail.com'
        text = '用户: ' + username + ' qq创建账号成功!' + 'ip地址为:' + ipaddr + '!' + 'qq昵称为:' + nickname
        send_mail = SendMail(subject, text, email)
        send_mail.start()


# 获取昵称
def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


# 获取用户名或昵称
def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


# 有昵称
def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


# 获取电话
def get_phone(self):
    if Phone_Profile.objects.filter(user=self).exists():
        phone_profile = Phone_Profile.objects.get(user=self)
        return phone_profile.phone
    else:
        return ''


User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username

User.get_phone = get_phone

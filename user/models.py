from django.db import models
from django.contrib.auth.models import User


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

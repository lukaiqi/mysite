import os
import shutil

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# 头像路径

AVATAR_ROOT = 'static/media/avatar'
AVATAR_DEFAULT = os.path.join(AVATAR_ROOT, 'default.png')


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


class Avatar(models.Model):
    """user avatar"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='头像')
    avatar = models.ImageField(upload_to=AVATAR_ROOT)

    class Meta:
        verbose_name = '头像'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Avatar:%s >' % (self.avatar)


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


# 动态绑定头像相关的方法
def get_avatar_url(self):
    try:
        avatar = Avatar.objects.get(user=self)
        return avatar.avatar
    except Exception:
        return AVATAR_DEFAULT


def set_avatar_url(self, src_path):
    try:
        avatar = Avatar.objects.filter(user=self.id)[0]
        old_path = os.path.join(settings.BASE_DIR, avatar.avatar.url)  # 旧的头像路径
        old_filename = os.path.splitext(os.path.split(old_path)[-1])[0]

        # 获得起始编号
        start_num = int(old_filename.split('_')[-1]) + 1
    except Exception:
        avatar = Avatar(user=self)
        start_num = 0
        old_path = ''

    # 根据user id设置新的头像名称
    filename = os.path.split(src_path)[-1]
    img_format = os.path.splitext(filename)[-1]

    while True:
        new_filename = '%s_64_%s%s' % (self.id, start_num, img_format)
        new_path = os.path.join(settings.BASE_DIR, AVATAR_ROOT, new_filename)
        if not os.path.isfile(new_path):
            break
        start_num += 1

    # 保存头像
    shutil.copy(src_path, new_path)
    avatar.avatar = os.path.join(AVATAR_ROOT, new_filename)
    avatar.save()

    # 删除旧文件
    if os.path.isfile(old_path):
        os.remove(old_path)
    return avatar


# 动态绑定方法
User.set_avatar_url = set_avatar_url

# 动态绑定方法
# User.get_avatar_url = MethodType(get_avatar_url, User)
User.get_avatar_url = get_avatar_url

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username

User.get_phone = get_phone

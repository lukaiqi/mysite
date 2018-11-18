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


# 访问网站的ip地址和次数
class Userip(models.Model):
    ip = models.CharField(verbose_name='IP地址', max_length=30)  # ip地址
    count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数

    class Meta:
        verbose_name = '访问ip统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


# 网站总访问次数
class VisitNumber(models.Model):

    site = models.CharField(verbose_name='站名', max_length=20, default='lkqblog.cn')
    count = models.IntegerField(verbose_name='网站总访次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站总访问数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站日访问量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)


def change_info(request):  # 修改网站访问量和访问ip等信息
    # 每一次访问，网站总访问次数加一
    count_nums = VisitNumber.objects.filter(site='lkqblog.cn')
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()

    # 记录访问ip和每个ip的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip
    # print(client_ip)

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:  # 判断是否存在该ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
    uobj.save()

    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()


# 统计
class Statistics(threading.Thread):
    def __init__(self, request):
        self.request = request
        threading.Thread.__init__(self)

    def run(self):
        change_info(self.request)

    def count(request):
        change_info = Statistics(request)
        change_info.start()


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

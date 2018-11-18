import threading
from django.db import models
from django.utils import timezone


# Create your models here.
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
    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:  # 判断是否存在该ip
        ip_num = ip_exist[0]
        ip_num.count += 1
    else:
        ip_num = Userip()
        ip_num.ip = client_ip
        ip_num.count = 1
        ip_num.save()
    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        day_num = today[0]
        day_num.count += 1
    else:
        day_num = DayNumber()
        day_num.dayTime = date
        day_num.count = 1
    day_num.save()


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

from django.shortcuts import render
from .models import VisitNumber, DayNumber, Userip


# Create your views here.
def count_show(request):
    if request.user.is_superuser:
        day_num = DayNumber.objects.all()  # 每日访问次数
        visit_num = VisitNumber.objects.all()  # 总访问次数
        ip_num = Userip.objects.all()  # ip访问次数
        content_day = list(day_num)
        content_num = list(visit_num)
        content_ip = list(ip_num)
        context = {}
        context['day'] = content_day
        context['visit'] = content_num
        context['ip'] = content_ip
        return render(request, 'visit/count_show.html', context)
    else:
        return render(request, 'error.html')

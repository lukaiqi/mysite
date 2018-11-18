from django.shortcuts import render
from .models import DayNumber, IpNumber, VisitNumber


# Create your views here.
def count_show(request):
    if request.user.is_superuser:
        day_num = DayNumber.objects.all()
        visit_num = VisitNumber.objects.all()
        ip_num = IpNumber.objects.all()
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

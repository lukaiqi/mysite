from django.shortcuts import render
from .models import About, Notice


# Create your views here.
def about(request):
    info = About.objects.all()
    context = {}
    context['info'] = info
    return render(request, 'info/about.html', context)


def get_notice():
    notice = Notice.objects.all().order_by('-creat_time')
    return notice

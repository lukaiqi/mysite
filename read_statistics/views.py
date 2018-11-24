from django.shortcuts import render
from .models import ReadDetail


# Create your views here.
def read_info(request):
    read_info = ReadDetail.objects.all()
    context = {}
    context['read_info'] = read_info
    return render(request, 'read_statistics/read_info.html', context)

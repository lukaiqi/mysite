from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Message


# Create your views here.
@csrf_exempt
def write(request):
    if request.method == 'POST':
        ds18b20value = request.POST.get('ds18b20value', '')
        dht11value = request.POST.get('dht11value', '')
        mq2value = request.POST.get('mq2value', '')
        lightvalue = request.POST.get('lightvalue', '')
        Message.objects.filter(id=1).update(ds18b20value=ds18b20value,
                                            dht11value=dht11value,
                                            mq2value=mq2value,
                                            lightvalue=lightvalue)
        return HttpResponse('success')


def show(request):
    if request.user.is_superuser:
        show_list = Message.objects.all()
        print(show_list)

        context = {}
        context['show_list'] = show_list
        return render(request, 'sensor/show.html', context)
    else:
        return render(request, 'error.html')


def ajax(request):
    ds18b20value = Message.objects.all().values('ds18b20value')[0].get('ds18b20value')
    dht11value = Message.objects.all().values('dht11value')[0].get('dht11value')
    mq2value = Message.objects.all().values('mq2value')[0].get('mq2value')
    lightvalue = Message.objects.all().values('lightvalue')[0].get('lightvalue')
    context = {}
    context['ds18b20value'] = ds18b20value
    context['dht11value'] = dht11value
    context['mq2value'] = mq2value
    context['lightvalue'] = lightvalue
    return JsonResponse(context)

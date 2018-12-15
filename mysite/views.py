import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'home.html')


@csrf_exempt
def tuling(request):
    name = request.POST.get('userId')
    text = request.POST.get('text')
    url = "http://openapi.tuling123.com/openapi/api/v2"
    payload = "{" \
              "\"perception\": {" \
              "\"inputText\": {" \
              "\"text\":" + repr(str(text.encode('utf-8'))) + \
              "}," \
              "}," \
              "\"userInfo\": {" \
              "\"apiKey\": \"67fd8719169c41d6805c83e267edba24\"," \
              "\"userId\":" + repr(name) + \
              "}" \
              "}"
    headers = {
        'content-type': "application/json",
        'charset': "utf-8",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return HttpResponse(response.text)

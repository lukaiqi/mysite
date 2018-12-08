import os
from os import listdir
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.utils.encoding import escape_uri_path


def upload_file(request):
    if request.user.is_superuser:
        if request.method == "POST":  # 请求方法为POST时，进行处理
            myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("未选择上传文件")
            destination = open(os.path.join("/home/mysite/files", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            return redirect('/file/file_list')
    else:
        return render(request, 'error.html')


def upload(request):
    return render(request, 'file/file_upload.html')


def file_list(request):
    if request.user.is_superuser:
        file_path = '/home/mysite/files/'
        file_name_list = listdir(file_path)
        context = {}
        context['file_name_list'] = file_name_list
        return render(request, 'file/files.html', context)
    else:
        return render(request, 'error.html')


def file_download(request):
    name = request.GET.get('filename')
    base_path = '/home/mysite/files/'
    file_path = base_path + name
    file = open(file_path, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(name))
    return response


def file_delete(request):
    name = request.GET.get('filename')
    base_path = '/home/mysite/files/'
    file_path = base_path + name
    os.remove(file_path)
    return render(request, 'file/file_del.html')

from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('file_download', views.file_download, name='file_download'),
    path('file_list', views.file_list, name='file_list'),
    path('file_delete', views.file_delete, name='file_delete'),
]

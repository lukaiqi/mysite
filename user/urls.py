from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('change_email/', views.change_email, name='change_email'),
    path('bind_phone/', views.bind_phone, name='bind_phone'),
    path('get_ip/', views.get_ip, name='get_ip'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('upload/', views.upload, name='upload'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('file_download/', views.file_download, name='file_download'),
    path('file_list/', views.file_list, name='file_list'),
    path('list_json/', views.list_json, name='list_json'),
    path('qq_login/', views.qq_login, name='qq_login'),
    path('qq_save/', views.qq_save, name='qq_save'),
]

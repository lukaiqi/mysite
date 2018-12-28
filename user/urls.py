from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('user_info', views.user_info, name='user_info'),
    path('change_nickname', views.change_nickname, name='change_nickname'),
    path('change_email', views.change_email, name='change_email'),
    path('bind_phone', views.bind_phone, name='bind_phone'),
    path('change_phone', views.change_phone, name='change_phone'),
    path('send_msg_verification_code', views.send_msg_verification_code, name='send_msg_verification_code'),
    path('send_email_verification_code', views.send_email_verification_code, name='send_email_verification_code'),
    path('change_password', views.change_password, name='change_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('user_avatar', views.user_avatar, name='user_avatar'),
    path('user_avatar_upload', views.user_avatar_upload, name='user_avatar_upload'),
]

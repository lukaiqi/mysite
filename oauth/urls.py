from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('qq_login', views.qq_login, name='qq_login'),
    path('qq_check', views.qq_check, name='qq_check'),
    path('bind_email', views.bind_email, name='bind_email'),
]

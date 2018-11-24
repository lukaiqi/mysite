from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('read_info', views.read_info, name='read_info'),
]

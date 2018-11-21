from django.urls import path
from . import views

urlpatterns = [
    path('count_show', views.count_show, name='count_show'),
]

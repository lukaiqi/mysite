from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('write/', views.write, name='write'),
    path('show/', views.show, name='show'),
    path('ajax/', views.ajax, name='ajax'),
]

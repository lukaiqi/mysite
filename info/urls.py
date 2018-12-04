from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('about', views.about, name='about'),
]

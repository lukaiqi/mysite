from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog_search', views.blog_search, name='blog_search'),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
]

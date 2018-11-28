from django.contrib import admin
from .models import About, Notice


# Register your models here.
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('creat_time', 'content')

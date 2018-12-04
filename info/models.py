from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class About(models.Model):
    text = RichTextUploadingField()

    class Meta:
        verbose_name = '关于'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Text:%s >' % (self.text)


class Notice(models.Model):
    creat_time = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=100)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Text:%s >' % (self.content)

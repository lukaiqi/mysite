from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class OAuth_ex(models.Model):
    """User models ex"""
    user = models.ForeignKey(User)  # 和User关联的外键
    qq_openid = models.CharField(max_length=64)  # QQ的关联OpenID

    def __str__(self):
        return u'<%s>' % (self.user)

from django.db import models


# Create your models here.
class Message(models.Model):
    ds18b20value = models.CharField(max_length=10)
    dht11value = models.CharField(max_length=10)
    mq2value = models.CharField(max_length=10)
    lightvalue = models.CharField(max_length=10)

# Generated by Django 2.1.1 on 2018-11-17 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_daynumber_userip_visitnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitnumber',
            name='site',
            field=models.CharField(default='lkqblog.cn', max_length=20, verbose_name='站名'),
        ),
    ]
# Generated by Django 2.1.1 on 2018-11-28 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20181118_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='info',
            name='user',
        ),
        migrations.DeleteModel(
            name='Info',
        ),
    ]
# Generated by Django 2.1.1 on 2018-11-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20181116_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='send_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 2.1.1 on 2018-11-18 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20181118_1427'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DayNumber',
        ),
        migrations.DeleteModel(
            name='Userip',
        ),
        migrations.DeleteModel(
            name='VisitNumber',
        ),
    ]

# Generated by Django 2.1.1 on 2018-10-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds18b20value', models.CharField(default=0, max_length=10)),
                ('dht11value', models.CharField(default=0, max_length=10)),
                ('mq2value', models.CharField(default=0, max_length=10)),
                ('lightvalue', models.CharField(default=0, max_length=10)),
            ],
        ),
    ]
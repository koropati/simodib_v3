# Generated by Django 2.2.2 on 2019-08-05 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0012_takendistribution_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takendistribution',
            name='test',
        ),
    ]

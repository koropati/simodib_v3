# Generated by Django 2.2.2 on 2019-09-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0014_auto_20190805_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='takendistribution',
            name='status_track',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]

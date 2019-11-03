# Generated by Django 2.2.6 on 2019-11-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0015_takendistribution_status_track'),
    ]

    operations = [
        migrations.AddField(
            model_name='distribution',
            name='catatan_khusus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='distribution',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='distribution',
            name='telepon',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]

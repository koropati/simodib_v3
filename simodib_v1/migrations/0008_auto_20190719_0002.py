# Generated by Django 2.2.2 on 2019-07-18 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0007_auto_20190719_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailorder',
            name='prices',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailorder',
            name='value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rice',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='rice',
            name='stock',
            field=models.IntegerField(),
        ),
    ]
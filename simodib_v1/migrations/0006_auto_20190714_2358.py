# Generated by Django 2.2.2 on 2019-07-14 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0005_auto_20190714_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailorder',
            name='prices',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='takendistribution',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='takendistribution',
            name='status',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.CreateModel(
            name='DataLogPerjalanan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('x', models.TextField(blank=True, null=True)),
                ('y', models.TextField(blank=True, null=True)),
                ('z', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('taken_distribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datalog_perjalanan', to='simodib_v1.TakenDistribution')),
            ],
        ),
    ]

# Generated by Django 2.2.2 on 2019-07-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simodib_v1', '0002_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortalSignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_kurir', models.CharField(max_length=1)),
                ('port_manager', models.CharField(max_length=1)),
                ('port_admin', models.CharField(max_length=1)),
            ],
        ),
    ]

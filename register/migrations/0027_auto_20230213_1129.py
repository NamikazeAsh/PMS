# Generated by Django 3.0.8 on 2023-02-13 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0026_auto_20230209_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='img',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='project',
        ),
    ]

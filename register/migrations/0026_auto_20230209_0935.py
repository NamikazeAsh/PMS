# Generated by Django 3.0.8 on 2023-02-09 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20230209_0935'),
        ('register', '0025_auto_20230208_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='company',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
# Generated by Django 4.1.2 on 2023-04-14 06:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0030_alter_requestmodel_reqdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='reqdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 14, 11, 59, 18, 256675), max_length=100),
        ),
    ]

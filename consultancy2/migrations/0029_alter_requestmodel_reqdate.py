# Generated by Django 4.1.2 on 2023-04-13 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0028_alter_requestmodel_reqdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestmodel',
            name='reqdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 13, 12, 17, 26, 476709), max_length=100),
        ),
    ]
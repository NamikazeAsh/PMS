# Generated by Django 4.1.7 on 2023-03-09 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0011_delete_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminvalidation',
            name='firstname',
            field=models.CharField(default='-', max_length=100),
        ),
        migrations.AddField(
            model_name='adminvalidation',
            name='lastname',
            field=models.CharField(default='-', max_length=100),
        ),
    ]

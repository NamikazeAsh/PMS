# Generated by Django 4.1.7 on 2023-03-09 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0012_adminvalidation_firstname_adminvalidation_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='signininsert',
            name='firstname',
            field=models.CharField(default='-', max_length=100),
        ),
        migrations.AddField(
            model_name='signininsert',
            name='lastname',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
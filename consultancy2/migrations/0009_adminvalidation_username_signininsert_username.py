# Generated by Django 4.0.1 on 2023-02-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0008_remove_adminvalidation_freehours'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminvalidation',
            name='username',
            field=models.CharField(default='-', max_length=100),
        ),
        migrations.AddField(
            model_name='signininsert',
            name='username',
            field=models.CharField(default='-', max_length=100),
        ),
    ]

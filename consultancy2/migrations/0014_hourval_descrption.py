# Generated by Django 4.0.1 on 2023-03-25 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0013_signininsert_firstname_signininsert_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='hourval',
            name='descrption',
            field=models.CharField(default='-', max_length=100),
        ),
    ]
# Generated by Django 4.0.1 on 2023-02-04 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamrecommender', '0006_auto_20230204_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userindex',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userscore',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

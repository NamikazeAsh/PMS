# Generated by Django 4.1.5 on 2023-02-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0026_auto_20230209_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, to='register.userprofile'),
        ),
    ]

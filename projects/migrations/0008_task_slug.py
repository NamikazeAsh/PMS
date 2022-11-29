# Generated by Django 4.0.8 on 2022-11-04 18:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_remove_task_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=250, unique_for_date=3),
            preserve_default=False,
        ),
    ]

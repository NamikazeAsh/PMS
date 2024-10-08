# Generated by Django 3.0.8 on 2023-01-31 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0018_auto_20230131_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='project',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='assign',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]

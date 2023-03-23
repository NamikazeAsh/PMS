# Generated by Django 4.1.7 on 2023-03-21 08:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendarapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventmember',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='eventmember',
            name='user',
        ),
        migrations.AddField(
            model_name='eventmember',
            name='user',
            field=models.ManyToManyField(related_name='event_members', to=settings.AUTH_USER_MODEL),
        ),
    ]

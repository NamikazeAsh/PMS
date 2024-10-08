# Generated by Django 4.0.1 on 2023-02-13 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0022_auto_20230209_0935'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0028_delete_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default='core/avatar/blank_profile.png', upload_to='core/avatar')),
                ('friends', models.ManyToManyField(blank=True, to='register.UserProfile')),
                ('project', models.ManyToManyField(blank=True, to='projects.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 4.0.1 on 2023-01-31 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_remove_team_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assign',
            field=models.ManyToManyField(to='projects.Team'),
        ),
    ]

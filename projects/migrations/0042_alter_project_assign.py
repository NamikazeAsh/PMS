# Generated by Django 4.0.1 on 2023-04-02 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_project_dead_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assign',
            field=models.ManyToManyField(blank=True, null=True, to='projects.Team'),
        ),
    ]

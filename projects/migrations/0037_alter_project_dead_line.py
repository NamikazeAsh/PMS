# Generated by Django 4.1.7 on 2023-03-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_alter_project_dead_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dead_line',
            field=models.DateField(),
        ),
    ]

# Generated by Django 4.1.7 on 2023-03-24 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_remove_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('1', 'Working'), ('2', 'Stuck'), ('3', 'Done')], default=1, max_length=7),
        ),
    ]

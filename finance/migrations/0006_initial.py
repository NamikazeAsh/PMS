# Generated by Django 4.1.2 on 2023-02-24 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0031_csv'),
        ('finance', '0005_delete_financemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt_received', models.FloatField(default=0)),
                ('cu_percentage', models.FloatField(default=0)),
                ('expenses', models.JSONField()),
                ('income', models.JSONField()),
                ('net_amt', models.FloatField(default=0)),
                ('professor', models.JSONField()),
                ('project_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]

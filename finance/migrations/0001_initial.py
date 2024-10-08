
# Generated by Django 4.1.5 on 2023-02-21 04:39

from django.db import migrations, models
import django.db.models.deletion
# Generated by Django 3.0.8 on 2023-02-21 04:58

from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    initial = True

    # dependencies = [
    #     ('projects', '0026_alter_project_documents'),
    #     ('projects', '0027_auto_20230220_1840'),

    # ]

    operations = [
        migrations.CreateModel(
            name='ProjectFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt_received', models.FloatField(default=0)),
                ('cu_percentage', models.FloatField(default=0)),
                ('expenses', models.JSONField()),
                ('income', models.JSONField()),
                ('net_amt', models.FloatField(default=0)),
                ('professor', models.JSONField()),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]

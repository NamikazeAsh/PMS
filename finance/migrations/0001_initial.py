<<<<<<< HEAD
# Generated by Django 4.1.5 on 2023-02-21 04:39

from django.db import migrations, models
import django.db.models.deletion
=======
<<<<<<< HEAD
# Generated by Django 3.0.8 on 2023-02-21 04:58

from django.db import migrations, models
import django.db.models.deletion
=======
# Generated by Django 4.0.1 on 2023-02-20 14:12

from django.db import migrations, models
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
>>>>>>> 8c60600770f97ce215616118a91193f660dd4b6d


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('projects', '0026_alter_project_documents'),
=======
<<<<<<< HEAD
        ('projects', '0027_auto_20230220_1840'),
=======
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
>>>>>>> 8c60600770f97ce215616118a91193f660dd4b6d
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='ProjectFinance',
            fields=[
=======
<<<<<<< HEAD
            name='ProjectFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt_received', models.FloatField(default=0)),
                ('cu_percentage', models.FloatField(default=0)),
                ('net_amt', models.FloatField(default=0)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
=======
            name='Finance',
            fields=[
>>>>>>> 8c60600770f97ce215616118a91193f660dd4b6d
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amt_received', models.FloatField(default=0)),
                ('cu_percentage', models.FloatField(default=0)),
                ('expenses', models.JSONField()),
                ('income', models.JSONField()),
                ('net_amt', models.FloatField(default=0)),
                ('professor', models.JSONField()),
<<<<<<< HEAD
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
=======
>>>>>>> 28f9b53e2ce6269cd38951cf7aac1aa71ba62bd1
>>>>>>> 8c60600770f97ce215616118a91193f660dd4b6d
            ],
        ),
    ]

# Generated by Django 4.1.5 on 2023-03-21 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_alter_financemodel_expenses_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financemodel',
            name='expenses',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='financemodel',
            name='income',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='financemodel',
            name='professor',
            field=models.JSONField(null=True),
        ),
    ]

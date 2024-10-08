# Generated by Django 4.1.2 on 2023-04-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_rename_income_financemodel_incomes'),
    ]

    operations = [
        migrations.AddField(
            model_name='financemodel',
            name='total_expenses',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='financemodel',
            name='total_incomes',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='financemodel',
            name='net_amt',
            field=models.FloatField(default=0, null=True),
        ),
    ]

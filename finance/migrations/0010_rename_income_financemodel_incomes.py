# Generated by Django 4.1.5 on 2023-03-23 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_rename_amt_received_financemodel_amtreceived_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='financemodel',
            old_name='income',
            new_name='incomes',
        ),
    ]

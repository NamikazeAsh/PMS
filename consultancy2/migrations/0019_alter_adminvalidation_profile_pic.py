# Generated by Django 4.1.7 on 2023-04-08 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultancy2', '0018_adminvalidation_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminvalidation',
            name='profile_pic',
            field=models.ImageField(blank=True, default='https://as1.ftcdn.net/v2/jpg/00/64/67/52/1000_F_64675209_7ve2XQANuzuHjMZXP3aIYIpsDKEbF5dD.jpg', upload_to='images/profile_pics/'),
        ),
    ]
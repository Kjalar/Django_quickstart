# Generated by Django 3.2 on 2021-04-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0009_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
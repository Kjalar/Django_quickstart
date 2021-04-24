# Generated by Django 3.2 on 2021-04-23 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0005_auto_20210422_0654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='tweet',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='photo',
            field=models.URLField(blank=True),
        ),
    ]

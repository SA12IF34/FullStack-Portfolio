# Generated by Django 4.2.2 on 2023-09-27 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0009_follownotification_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follownotification',
            name='target',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='follownotification',
            name='username',
            field=models.CharField(max_length=200),
        ),
    ]

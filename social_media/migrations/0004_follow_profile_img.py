# Generated by Django 4.2.2 on 2023-07-29 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0003_alter_post_options_alter_comment_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='profile_img',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]

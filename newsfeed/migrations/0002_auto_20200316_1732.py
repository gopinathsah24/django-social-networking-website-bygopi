# Generated by Django 3.0.3 on 2020-03-16 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(default='avatars/default.jpg', upload_to='avatars'),
        ),
    ]

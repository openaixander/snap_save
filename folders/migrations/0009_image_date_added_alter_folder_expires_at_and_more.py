# Generated by Django 4.2.11 on 2024-05-24 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0008_remove_uploadimage_images_alter_folder_expires_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default='2023-12-12'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='folder',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 26, 6, 3, 40, 334399, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images_uploaded'),
        ),
    ]

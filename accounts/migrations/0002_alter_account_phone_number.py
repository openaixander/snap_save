# Generated by Django 4.2.11 on 2024-05-12 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]

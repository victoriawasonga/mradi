# Generated by Django 5.2.1 on 2025-05-18 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='mradi/profile_pictures/'),
        ),
    ]

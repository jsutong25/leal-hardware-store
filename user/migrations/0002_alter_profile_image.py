# Generated by Django 5.0.4 on 2024-04-27 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='defaultprofile.jpg', upload_to='profile_images'),
        ),
    ]

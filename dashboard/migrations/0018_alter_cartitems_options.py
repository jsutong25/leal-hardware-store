# Generated by Django 5.0.4 on 2024-05-03 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_remove_cartitems_cart_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitems',
            options={'verbose_name_plural': 'Carts'},
        ),
    ]
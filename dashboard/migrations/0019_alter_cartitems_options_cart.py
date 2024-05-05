# Generated by Django 5.0.4 on 2024-05-03 00:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_alter_cartitems_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitems',
            options={'verbose_name_plural': 'Cart Items'},
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.PositiveBigIntegerField(default=490646)),
                ('items', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.cartitems')),
            ],
        ),
    ]

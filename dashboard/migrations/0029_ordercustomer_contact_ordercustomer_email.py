# Generated by Django 5.0.4 on 2024-05-04 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_ordercustomer_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercustomer',
            name='contact',
            field=models.IntegerField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ordercustomer',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]

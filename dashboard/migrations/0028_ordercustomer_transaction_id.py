# Generated by Django 5.0.4 on 2024-05-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_delete_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercustomer',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

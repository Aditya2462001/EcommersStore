# Generated by Django 3.2.6 on 2022-01-07 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0023_rename_customer_productrequest_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productrequest',
            old_name='customer_id',
            new_name='customer',
        ),
    ]

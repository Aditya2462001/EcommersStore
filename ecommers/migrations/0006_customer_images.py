# Generated by Django 3.2.6 on 2021-12-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0005_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='customer'),
        ),
    ]

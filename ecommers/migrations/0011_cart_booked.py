# Generated by Django 3.2.6 on 2021-12-29 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0010_products_product_image4'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 3.2.6 on 2021-12-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0004_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
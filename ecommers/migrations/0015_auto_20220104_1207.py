# Generated by Django 3.2.6 on 2022-01-04 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0014_auto_20220102_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbooking',
            name='razorpay_orderId',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='productbooking',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]

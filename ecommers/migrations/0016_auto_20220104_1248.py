# Generated by Django 3.2.6 on 2022-01-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0015_auto_20220104_1207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbooking',
            name='cart',
        ),
        migrations.AddField(
            model_name='productbooking',
            name='cart',
            field=models.ManyToManyField(blank=True, null=True, to='ecommers.Cart'),
        ),
    ]

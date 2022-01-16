# Generated by Django 3.2.7 on 2021-11-26 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='stock_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productbooking',
            name='product',
            field=models.ManyToManyField(blank=True, to='ecommers.Products'),
        ),
    ]
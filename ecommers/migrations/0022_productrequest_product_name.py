# Generated by Django 3.2.6 on 2022-01-07 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0021_auto_20220107_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrequest',
            name='product_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]

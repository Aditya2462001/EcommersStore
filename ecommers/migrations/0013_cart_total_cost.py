# Generated by Django 3.2.6 on 2021-12-31 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommers', '0012_auto_20211229_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_cost',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

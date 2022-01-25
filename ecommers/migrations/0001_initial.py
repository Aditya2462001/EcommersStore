# Generated by Django 3.2.6 on 2022-01-25 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total_cost', models.CharField(blank=True, max_length=50, null=True)),
                ('booked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=5000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category-img/')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('number', models.CharField(blank=True, max_length=12, null=True)),
                ('email', models.EmailField(blank=True, max_length=256, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='customer')),
                ('otp', models.CharField(blank=True, max_length=50, null=True)),
                ('verify_email', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=500, null=True)),
                ('product_slug', models.SlugField(blank=True, null=True)),
                ('product_desc', models.TextField(blank=True, null=True)),
                ('product_feature', models.TextField(blank=True, null=True)),
                ('product_rating', models.IntegerField(blank=True, null=True)),
                ('rate', models.IntegerField(blank=True, null=True)),
                ('selling_rate', models.IntegerField(blank=True, null=True)),
                ('stock_count', models.IntegerField(blank=True, null=True)),
                ('available', models.BooleanField(blank=True, default=True, null=True)),
                ('product_date', models.DateField(auto_now_add=True)),
                ('product_image1', models.ImageField(blank=True, null=True, upload_to='productImages/')),
                ('product_image2', models.ImageField(blank=True, null=True, upload_to='productImages/')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to='productImages/')),
                ('product_image4', models.ImageField(blank=True, null=True, upload_to='productImages/')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ecommers.category')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=50, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.products')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('product_name', models.TextField(blank=True, null=True)),
                ('product_id', models.CharField(blank=True, max_length=50000, null=True)),
                ('defect_info', models.TextField(blank=True, null=True)),
                ('request_action', models.CharField(blank=True, max_length=100, null=True)),
                ('accept_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('return_payment', models.CharField(blank=True, max_length=5000, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=500, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('total_amount', models.IntegerField(blank=True, null=True)),
                ('payment_type', models.CharField(blank=True, max_length=500, null=True)),
                ('booking_id', models.CharField(blank=True, max_length=50, null=True)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('delivary_status', models.CharField(blank=True, max_length=1000, null=True)),
                ('booking_status', models.BooleanField(blank=True, default=False, null=True)),
                ('razorpay_orderId', models.CharField(blank=True, max_length=10000, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=1000, null=True)),
                ('payment_status', models.CharField(blank=True, max_length=1000, null=True)),
                ('cart', models.ManyToManyField(blank=True, to='ecommers.Cart')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.customer')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommers.products'),
        ),
    ]

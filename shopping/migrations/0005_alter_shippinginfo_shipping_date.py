# Generated by Django 4.2.1 on 2023-06-13 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_order_product_amount_alter_customer_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippinginfo',
            name='shipping_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
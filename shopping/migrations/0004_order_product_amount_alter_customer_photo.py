# Generated by Django 4.2.1 on 2023-06-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_alter_product_photo_alter_productphoto_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_product',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
    ]

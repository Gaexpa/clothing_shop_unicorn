# Generated by Django 4.2.1 on 2023-06-10 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('knit', '針織衫'), ('shirt', '襯衫'), ('sweat', '大學T'), ('t_shirt', 'T恤'), ('tank_top', '吊帶背心'), ('vest', '背心'), ('jacket', '夾克'), ('cardigan', '開襟衫'), ('coat', '大衣'), ('knit_dress', '針織洋裝'), ('long_dress', '長洋裝'), ('shirt_dress', '短洋裝'), ('cami_dress', '細肩帶洋裝'), ('pants', '長褲'), ('shorts', '短褲'), ('skirt', '裙子')], max_length=50),
        ),
    ]
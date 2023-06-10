from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#客人
#客人與原生User 一對一關係，User新增、更新時其對應Customer也會新增更新
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    photo = models.ImageField(upload_to='images/', default='default.jpg')
    color_list=[('P', '紫色'), ('R', '紅色'), ('Y', '黃色'), ('B', '藍色'), ('G', '綠色')]
    color = models.CharField(default='P', choices=color_list, max_length=3)

    def __str__(self):
        return f'{self.user.username, self.user.email, self.address, self.color}'


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

#商品
class Product(models.Model):
    name = models.CharField(max_length=128)
    category_list = [('knit', '針織衫'), ('shirt', '襯衫'), ('sweat', '大學T'), ('t_shirt', 'T恤'), ('tank_top', '吊帶背心'), ('vest', '背心'), 
                     ('jacket', '夾克'), ('cardigan', '開襟衫'), ('coat', '大衣'), 
                     ('knit_dress', '針織洋裝'), ('long_dress', '長洋裝'), ('shirt_dress', '短洋裝'), ('cami_dress', '細肩帶洋裝'),
                     ('pants', '長褲'), ('shorts', '短褲'), ('skirt', '裙子')]
    category = models.CharField(choices=category_list, max_length=50)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    sold_quantity = models.PositiveIntegerField(default=0)
    photo = models.URLField()
    size_list = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')]
    size = models.CharField(choices=size_list, max_length=3)
    color_list = [('black', '黑色'), ('blue', '藍色'), ('yellow', '黃色'), ('pink', '粉色'), ('brown', '深褐色'), ('beige', '淺棕色'), ('purple', '紫色'), ('green', '綠色'), ('white', '白色')]
    color = models.CharField(choices=color_list, max_length=10)

    def __str__(self):
        return f'{self.name, self.category, self.price, self.quantity, self.size, self.color}'

#商品相片集
class ProductPhoto(models.Model):
    photo = models.URLField()
    product = models.ManyToManyField(Product, through='ProductPhoto_Product', through_fields=('productPhoto', 'product'))

    def __str__(self):
        return f'{self.id}'

#商品與商品相片集
class ProductPhoto_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productPhoto = models.ForeignKey(ProductPhoto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product, self.productPhoto}'


# 關注清單
class FollowList(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='FollowList_Product', through_fields=('followList', 'product'))

    def __str__(self):
        return f'{self.customer}'

# receiver使sender model(這邊是Customer)一被建立，FollowList也會建立
@receiver(post_save, sender=Customer)
def create_follow_list(sender, instance, created, **kwargs):
    if created:
        FollowList.objects.create(customer=instance)

# 關注清單與商品 多對多的中間資料表
class FollowList_Product(models.Model):
    followList = models.ForeignKey(FollowList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.followList, self.product}'
    


#購物車
class ShoppingCart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ShoppingCart_Product', through_fields=('shoppingCart','product'))

    def __str__(self):
        return f'{self.customer, self.customer.user.username}'

@receiver(post_save, sender=Customer)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(customer=instance)

#購物車與商品 多對多的中間資料表
class ShoppingCart_Product(models.Model):
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.shoppingCart, self.product}'



#訂單
class Order(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='Order_Product', through_fields=('order', 'product'))
    created_date = models.DateField(auto_now_add=True)
    status_list=[('unfinished', '未完成'), ('finished', '完成')]
    status = models.CharField(default='unfinished', choices=status_list, max_length=20)

    def __str__(self):
        return f'{self.customer, self.created_date, self.status}'

#訂單與商品 多對多的中間資料表
class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.order, self.product}'


#留言
class Comment(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    class Rate(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    rate = models.IntegerField(choices=Rate.choices)
    content = models.TextField(max_length=255)

    def __str__(self):
        return f'{self.customer, self.product, self.rate}'

#運送資訊單
class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    shipping_date = models.DateField()
    shipping_cost = models.PositiveIntegerField(default=0)
    shipping_address = models.CharField(max_length=128)
    shipping_status_list = [('undelivered', '尚未發貨'), ('delivering', '送貨中'), ('delivered', '已送達')]
    shipping_status = models.CharField(default='undelivered', choices=shipping_status_list, max_length=20)

    def __str__(self):
        return f'{self.order, self.receiver, self.phone, self.shipping_date, self.shipping_cost, self.shipping_address, self.shipping_status}'
    
@receiver(post_save, sender=Order)
def create_shipping_info(sender, instance, created, **kwargs):
    if created:
        ShippingInfo.objects.create(order = instance)

#結帳資訊單
class PaymentInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payer = models.CharField(max_length=50)
    payment_method_list = [('visa', 'Visa'), ('transfer', '匯款'), ('COD', '貨到付款')]
    payment_method = models.CharField(choices=payment_method_list, max_length=10)
    payment_status_list = [('unpaid', '未付款'), ('paid', '已付款')]
    payment_status = models.CharField(default='unpaid', choices=payment_status_list, max_length=10)

    def __str__(self):
        return f'{self.order, self.payer, self.payment_method, self.payment_status}'

@receiver(post_save, sender=Order)
def create_payment_info(sender, instance, created, **kwargs):
    if created:
        PaymentInfo.objects.create(order = instance)
from django.contrib import admin
from .models import Customer, Product, ProductPhoto, ProductPhoto_Product, FollowList, FollowList_Product, ShoppingCart, ShoppingCart_Product, Order, Order_Product, Comment, ShippingInfo, PaymentInfo

# Register your models here.
# 客人
class CustomerAdmin(admin.ModelAdmin):
    list_display=('user', 'address', 'color')
admin.site.register(Customer, CustomerAdmin)

# 商品與商品相片集、他們的多對多中間表
class ProductAdmin(admin.ModelAdmin):
    list_display=('name', 'category', 'price', 'quantity', 'sold_quantity', 'photo', 'size', 'color')
admin.site.register(Product, ProductAdmin)

class ProductPhotoAdmin(admin.ModelAdmin):
    list_display=('id', 'photo')
admin.site.register(ProductPhoto, ProductPhotoAdmin)

class ProductPhoto_ProductAdmin(admin.ModelAdmin):
    list_display=('product', 'productPhoto')
admin.site.register(ProductPhoto_Product, ProductPhoto_ProductAdmin)

# 關注清單、關注清單與商品多對多中間表
class FollowListAdmin(admin.ModelAdmin):
    list_display=('id', 'customer')
admin.site.register(FollowList, FollowListAdmin)

class FollowList_ProductAdmin(admin.ModelAdmin):
    list_display=('followList', 'product')
admin.site.register(FollowList_Product, FollowList_ProductAdmin)

# 購物車、購物車與商品多對多中間表
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display=('id', 'customer')
admin.site.register(ShoppingCart, ShoppingCartAdmin)

class ShoppingCart_ProductAdmin(admin.ModelAdmin):
    list_display=('shoppingCart', 'product')
admin.site.register(ShoppingCart_Product, ShoppingCart_ProductAdmin)

# 訂單、訂單與商品多對多中間表
class OrderAdmin(admin.ModelAdmin):
    list_display=('id', 'customer', 'created_date', 'status')
admin.site.register(Order, OrderAdmin)

class Order_ProductAdmin(admin.ModelAdmin):
    list_display=('order', 'product')
admin.site.register(Order_Product, Order_ProductAdmin)

# 留言
class CommentAdmin(admin.ModelAdmin):
    list_display=('customer', 'product', 'rate')
admin.site.register(Comment, CommentAdmin)

# 運送資訊單
class ShippingInfoAdmin(admin.ModelAdmin):
    list_display=('order', 'receiver', 'phone', 'shipping_date', 'shipping_cost', 'shipping_status')
admin.site.register(ShippingInfo, ShippingInfoAdmin)

# 付款資訊單
class PaymentInfoAdmin(admin.ModelAdmin):
    list_display=('order', 'payer', 'payment_method', 'payment_status')
admin.site.register(PaymentInfo, PaymentInfoAdmin)
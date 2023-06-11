from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Customer, Product, ProductPhoto, ProductPhoto_Product, FollowList, FollowList_Product, ShoppingCart, ShoppingCart_Product, Order, Order_Product, Comment, ShippingInfo, PaymentInfo

# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    new_products = Product.objects.raw('SELECT * FROM shopping_product GROUP BY name ORDER BY id DESC LIMIT 10')
    #new_products = Product.objects.order_by("-id").values('name').distinct()[:10]
    best_selling_products = Product.objects.raw('SELECT id, name, category, price, SUM(sold_quantity) AS sold_quantity, photo FROM shopping_product GROUP BY name ORDER BY sold_quantity DESC LIMIT 10')
    #best_selling_products = Product.objects.order_by("-sold_quantity").values('name').distinct("name")[:10]

    context = {
        'new_products' : new_products,
        'best_selling_products' : best_selling_products,
    }
    return HttpResponse(template.render(context, request))

def category_search(request, category):
    category_products = Product.objects.raw('SELECT * FROM shopping_product WHERE category = %s GROUP BY name', [category])
    # category的tuple list
    category_list = [('knit', '針織衫'), ('shirt', '襯衫'), ('sweat', '大學T'), ('t_shirt', 'T恤'), ('tank_top', '吊帶背心'), ('vest', '背心'), 
                        ('jacket', '夾克'), ('cardigan', '開襟衫'), ('coat', '大衣'), 
                        ('knit_dress', '針織洋裝'), ('long_dress', '長洋裝'), ('shirt_dress', '短洋裝'), ('cami_dress', '細肩帶洋裝'),
                        ('pants', '長褲'), ('shorts', '短褲'), ('skirt', '裙子')]
    for c in category_list:
        if c[0] == category:
            category_name = c[1]
    
    template = loader.get_template('category.html')

    context = {
        'category_products' : category_products,
        'category_name' : category_name
    }
    return HttpResponse(template.render(context, request))
    

def details(request, id):
    product = Product.objects.get(id=id)
    template = loader.get_template('details.html')

    # QuerySet是dict list
    # 顏色的tuple list
    color_list = [('black', '黑色'), ('blue', '藍色'), ('yellow', '黃色'), ('pink', '粉色'), ('brown', '深褐色'), ('beige', '淺棕色'), ('purple', '紫色'), ('green', '綠色'), ('white', '白色')]
    size_list = [('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')]
    product_dict_list = []  #product_dict_list會是雙層list，第一層[0], [1], [2], [3]...是以不同color分，[0][1], [0][2]...就是同色不同size
    for c in color_list:
        res = Product.objects.filter(name=product.name, color = c[0], quantity__gt = 0)
        if res:
            product_dict_list.append( res )  #如果沒有該顏色，QuerySet會回傳空值，所以篩掉沒有的顏色，且還有庫存
    
    first_range_list = range(0, len(product_dict_list))
    second_range_list = []  #紀錄size數量的list
    for i in first_range_list:
        second_range_list.append(range(0, len(product_dict_list[i])))
    
    list = [0, 1, 2, 3]
    context = {
        'product' : product,
        'product_dict_list' : product_dict_list,
        'first_range_list' : first_range_list,
        'second_range_list' : first_range_list,
        'list' : list,

    }
    return HttpResponse(template.render(context, request))
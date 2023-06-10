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

def category_search(request):
    pass

def details(request):
    pass
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import (
    Customer,
    Product,
    ProductPhoto,
    ProductPhoto_Product,
    FollowList,
    FollowList_Product,
    ShoppingCart,
    ShoppingCart_Product,
    Order,
    Order_Product,
    Comment,
    ShippingInfo,
    PaymentInfo,
)

# Create your views here.


def index(request):
    template = loader.get_template("index.html")
    new_products = Product.objects.raw(
        "SELECT * FROM shopping_product GROUP BY name ORDER BY id DESC LIMIT 10"
    )
    # new_products = Product.objects.order_by("-id").values('name').distinct()[:10]
    best_selling_products = Product.objects.raw(
        "SELECT id, name, category, price, SUM(sold_quantity) AS sold_quantity, photo FROM shopping_product GROUP BY name ORDER BY sold_quantity DESC LIMIT 10"
    )
    # best_selling_products = Product.objects.order_by("-sold_quantity").values('name').distinct("name")[:10]

    context = {
        "new_products": new_products,
        "best_selling_products": best_selling_products,
    }
    return HttpResponse(template.render(context, request))


def category_search(request):
    pass


def details(request):
    pass


def view_cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        cart_items = customer.shoppingcart.product.all()

        context = {
            "cart_items": cart_items,
        }
        return render(request, "cart.html", context)
    else:
        return redirect("login")  # 重定向到登录页面


def delete_item(request, item_id):
    if request.user.is_authenticated:  # 检查用户是否已登录
        customer = Customer.objects.get(user=request.user)
        shopping_cart = customer.shoppingcart
        item = shopping_cart.product.get(id=item_id)
        shopping_cart.product.remove(item)
        return redirect("cart")
    else:
        return redirect("login")  # 重定向到登录页面


def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        shopping_cart = customer.shoppingcart
        cart_items = customer.shoppingcart.product.all()

        unfinished_orders = Order.objects.filter(customer=customer, status="unfinished")
        if unfinished_orders.exists():
            order = unfinished_orders.first()
        else:
            # 创建新的订单
            order = Order.objects.create(customer=customer)

        if cart_items.exists():
            # 将购物车商品添加到订单中
            for item in cart_items:
                Order_Product.objects.create(order=order, product=item, amount=1)
            for item in cart_items:
                shopping_cart.product.remove(item)
            # 重定向到结账页面
            return redirect("order")
        else:
            # 购物车为空，无法结账
            return redirect("cart")
    else:
        return redirect("index")


def check_order(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        user = customer.user
        cart_items = customer.shoppingcart.product.all()
        order_items = customer.order.product.all()
        first_order = Order.objects.filter(customer=customer.id).first()
        amounts = Order_Product.objects.filter(order=first_order.id).all()

        total_price = 0
        for item in cart_items:
            total_price += item.price

        context = {
            "customer": customer,
            "cart_items": cart_items,
            "user": user,
            "amounts": amounts,
            "order_items": order_items,
            "total_price": total_price,
        }
        return render(request, "checkout.html", context)
    else:
        return redirect("cart")


def order(request):
    customer = Customer.objects.get(user=request.user)
    order_items = customer.order.product.all()
    context = {
        "order_items": order_items,
    }
    return render(request, "order.html", context)

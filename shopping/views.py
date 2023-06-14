from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Customer, Product, ProductPhoto, ProductPhoto_Product, FollowList, FollowList_Product, ShoppingCart, ShoppingCart_Product, Order, Order_Product, Comment, ShippingInfo, PaymentInfo
from django.contrib.auth import authenticate
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib import auth
from shopping.forms import RegistrationForm

# Create your views here.


def index(request):
    if 'color' not in request.session:
        request.session['test_answers'] = []
        request.session['test_answers']='rgb(160, 134, 180)'
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

def login(request):
    # 以登入就轉到訂單
    if request.user.is_authenticated:
        return redirect('order')
    
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request,username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    template = loader.get_template('login.html')
    context = {'form': form}
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def logout(request):
    auth.logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            address = form.cleaned_data['address']
            user_id = user.id 
            c=Customer.objects.get(id=user_id)
            c.address=address
            c.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request=request,username=username, password=password)
            if user is not None:
                auth.login(request,user)
            if 'test_answers' in request.session:
                 del request.session['test_answers']
            if 'total_score' in request.session:
                del request.session['total_score']
            return redirect('psychometric_test')
        
    else:
        form = RegistrationForm()
    template = loader.get_template('register.html')
    context = {'form': form}
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def psychometric_test(request):
    questions = [
        {'id': 1, 'text': '問題1:你喜歡哪個季節？', 'choices': {'春天':1, '夏天':2, '秋天':3,'冬天':4}},
        {'id': 2, 'text': '問題2:在霍格華茲魔法與巫術學院中探險吧！', 'choices': {'禁林':4, '天文塔':3, '溫室':1,'海格的小屋':2}},
        {'id': 3, 'text': '問題3:閒暇的周末請選擇一項安排', 'choices': {'豋山吸收芬多精':1, '製作和創造新的網站':3, '參加朋友舉辦的換裝派對':2,'追新出的動畫作品':4}},
    ]
    if request.method == 'POST':
        # 获取当前问题的回答
        answer = request.POST.get('answer')
        # 将回答存储在用户会话（session）中

        if 'test_answers' not in request.session:
            print('建立新test_answers\n')
            request.session['test_answers'] = []
        if 'total_score' not in request.session:
            print('建立新total_score\n')
            request.session['total_score'] =0
        request.session['test_answers'] =  request.session['test_answers'] + [answer]
        s='ans'+str(len(request.session['test_answers']))+'\n'
        print(s)
        print(request.session['test_answers'])
        s='total'+str(len(questions))
        print(s)
        #最後一題後顯示結果
        if len(request.session['test_answers']) == len(questions):
            request.session['total_score']  = 0
            for i, ans in enumerate(request.session['test_answers']):
                choice = questions[i]['choices'].get(ans)
                if choice:
                    request.session['total_score']  += choice
            print('enter1')
            template = loader.get_template('result.html')
            return redirect('result')
        else:
            print('enter2')
            next_question = questions[len(request.session['test_answers'])]
            template = loader.get_template('psychometric_test.html')
            return HttpResponse(template.render({'question': next_question}, request))
    

    first_question = questions[0]
    template = loader.get_template('psychometric_test.html')
    return HttpResponse(template.render({'question': first_question}, request))

def result(request):
    if request.user.is_authenticated:
        print('enter')
        answers = request.session.get('test_answers', [])  # 获取用户的答案列表
        total_score = request.session.get('total_score', 0)  # 获取总分
        c=Customer.objects.get(id=request.user.id)
        if c is not None:
            print("findc")
        if total_score%4==0:
            print("choice1")
            setattr(c,'color','R')
            c.address="apple"
            c.save()
        elif total_score%4==1:
            print("choice1")
            c.address="apple"
            setattr(c,'color','G')
            c.save()
        elif total_score%4==2:
            print("choice1")
            c.address="apple"
            setattr(c,'color','B')
            c.save()
        else:
            print("choice1")
            c.address="apple"
            setattr(c,'color','Y')
            c.save()
        request.session.pop('test_answers', None)
        request.session.pop('total_score', None)
        template = loader.get_template('result.html')
        return HttpResponse(template.render({'answers': answers, 'choice': c.color}, request))

    # 清空会话中的答案和总分
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))

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
    # 一般呈現商品細節
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
    
    # 加入購物車/關注清單
    if request.method == 'GET' and "size-select" in request.GET:
        customer = Customer.objects.get(user=request.user)
        p_id = request.GET.get("size-select")
        product = Product.objects.get(id = p_id)
        

        if 'follow_list' in request.GET:
            follow_list = FollowList.objects.get(customer = customer)
            FollowList_Product.objects.create(followList = follow_list, product = product)
        else:
            # 'cart' in request.GET
            cart = ShoppingCart.objects.get(customer = customer)
            ShoppingCart_Product.objects.create(shoppingCart = cart, product = product) 

    # context
    context = {
        'product' : product,
        'product_dict_list' : product_dict_list,
        'first_range_list' : first_range_list,
        'second_range_list' : first_range_list,
        'list' : list,

    }
    return HttpResponse(template.render(context, request))

def search(request):
    query = request.GET.get("search")
    products = None
    query = "%"+query+"%"
    products = Product.objects.raw('SELECT * FROM shopping_product WHERE name LIKE %s GROUP BY name', [query])
    #products = Product.objects.filter(name__icontains = query)
    context = {
        'products': products,
    }
    return render(request, 'search.html', context=context)


# 查看關注清單
def follow_list(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        follow_list_items = customer.followlist.product.all()

        context = {
            "items": follow_list_items,
        }
        return render(request, "follow_list.html", context)
    else:
        return redirect("login")  # 重定向到登录页面
    
def delete_follow_list_item(request, item_id):
    if request.user.is_authenticated:  # 检查用户是否已登录
        customer = Customer.objects.get(user=request.user)
        follow_list = customer.followlist
        item = follow_list.product.get(id=item_id)
        follow_list.product.remove(item)
        return redirect("follow_list")
    else:
        return redirect("login")  # 重定向到登录页面

# 查看購物車
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


def delete_cart_item(request, item_id):
    if request.user.is_authenticated:  # 检查用户是否已登录
        customer = Customer.objects.get(user=request.user)
        shopping_cart = customer.shoppingcart
        item = shopping_cart.product.get(id=item_id)
        shopping_cart.product.remove(item)
        return redirect("cart")
    else:
        return redirect("login")  # 重定向到登录页面

# 確認訂單資訊
def check_order(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        user = customer.user
        cart_items = customer.shoppingcart.product.all()
        total_price = 0
        for item in cart_items:
            total_price += item.price

        context = {
            "customer": customer,
            "cart_items": cart_items,
            "user": user,
            "total_price": total_price,
        }
        return render(request, "checkout.html", context)
    else:
        return redirect("cart")

# 下訂單
def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        shopping_cart = customer.shoppingcart
        cart_items = customer.shoppingcart.product.all()



        if cart_items.exists():  #購物車內有東西
            # 创建新的订单
            order = Order.objects.create(customer=customer)
            unfinished_orders = Order.objects.filter(customer=customer, status="unfinished")
            # 将购物车商品添加到订单中
            for item in cart_items:
                Order_Product.objects.create(order=order, product=item, amount=1)
            
            for item in cart_items:
                # 購買商品庫存減少
                target_product = Product.objects.get(id=item.id)
                order_product_amount = Order_Product.objects.get(order_id = order.id, product_id = item.id).amount
                target_product.quantity =  target_product.quantity - order_product_amount
                # 將購物車商品加到訂單後，刪除
                shopping_cart.product.remove(item)
            
            # 重定向到结账页面
            return redirect("order")
        else:
            # 购物车为空，无法结账
            return redirect("cart")

        

        # unfinished_orders = Order.objects.filter(customer=customer, status="unfinished")
        # if unfinished_orders.exists():
        #     order = unfinished_orders.first()
        # else:
        #     # 创建新的订单
        #     order = Order.objects.create(customer=customer)
        #     if cart_items.exists():
        #         # 将购物车商品添加到订单中
        #         for item in cart_items:
        #             Order_Product.objects.create(order=order, product=item, amount=1)
        #         for item in cart_items:
        #             shopping_cart.product.remove(item)
        #         # 重定向到结账页面
        #         return redirect("order")
        #     else:
        #         # 购物车为空，无法结账
        #         return redirect("cart")
    else:
        return redirect("index")


# 查看訂單
def order(request):
    # 找user的單，可能有很多張
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer = customer)

    # order_list放不同訂單, 每個訂單裡有product_list放不同商品
    order_list = []
    for o in orders:
        product_list = []
        order_products = Order_Product.objects.filter(order_id = o.id)
        for op in order_products:
            product = Product.objects.get(id = op.product_id)
            product_list.append(product)
        
        order_list.append(product_list)
        
    # # order_item_list是放訂單商品的list，order_item_list[n]是不同訂單
    # order_items_list = [][20]  #一張單商品數不能超過20，20可以改，但因為第二層要固定size所以才填數字
    # order_index = 0
    # for op in order_products:
    #     for line in op:
    #         product = Product.objects.get(id = line.product_id)
    #         order_items_list[order_index].append()
    #         order_index += 1
    


    # 發現model裡 Order.customer是OneToOneField(一對一)Customer，更改成ForeignKey
    # 因為一個客人不應該一次只能有一個訂單，應該可以有多個，改了後下面的會有錯
    # customer = Customer.objects.get(user=request.user)
    # order_items = customer.order.product.all()
    context = {
        "order_items" : order_list,
    }
    return render(request, "order.html", context)


from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib import auth
from shopping.forms import RegistrationForm
from shopping.models import Customer
from django.shortcuts import redirect

# Create your views here.
def index(request):
    template = loader.get_template('index.html')
    context = {'request': request}
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

def login(request):
    if request.method == 'POST':
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
        
        request.session['test_answers'] =  request.session['test_answers'] + [answer]
        s='ans'+str(len(request.session['test_answers']))+'\n'
        print(s)
        print(request.session['test_answers'])
        s='total'+str(len(questions))
        print(s)
        #最後一題後顯示結果
        if len(request.session['test_answers']) == len(questions):
            total_score = 0
            for i, ans in enumerate(request.session['test_answers']):
                choice = questions[i]['choices'].get(ans)
                if choice:
                    total_score += choice
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
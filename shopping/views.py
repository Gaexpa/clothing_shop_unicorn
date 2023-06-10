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
    template = loader.get_template('register.html')
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
            print('enters')
            user = form.save()
            address = form.cleaned_data['address']
            user_id = user.id 
            c=Customer.objects.get(id=user_id)
            c.address=address
            c.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    template = loader.get_template('register.html')
    context = {'form': form}
    rendered_template = template.render(context, request)
    return HttpResponse(rendered_template)

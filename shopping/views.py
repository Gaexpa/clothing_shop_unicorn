from django.http import HttpResponse
from django.template import loader
from shopping.forms import RegistrationForm
from shopping.models import Customer
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return HttpResponse("你好")

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

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
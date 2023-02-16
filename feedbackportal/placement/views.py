from django.shortcuts import render
from django.http import HttpResponse
from .models import Carausel 
#from django.views.generic import CreateView
from django.template import loader
from django.http import HttpResponseRedirect
#from .forms import RegisterForm
from django.contrib.auth.models import User


def placement(request):
    template = loader.get_template('main/homepage.html')
    return HttpResponse(template.render())

def main(request):
    obj = Carausel.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'main/home.html',context)
  

def detail(request):
    template = loader.get_template('main/detail.html')
    return HttpResponse(template.render())
   
def register(request):
    return render(request,template_name="main/register.html")

def about(request):
    return render(request,"main/about.html")

def profile(request):
    return render(request,"main/profile.html")
    
def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'main/register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
               
                # Login the user
                login(request, user)
               
                # redirect to accounts page:
                return HttpResponseRedirect('/mymodule/account')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})
#def studentview(CreateView):
 #   model = Students
  #  fields = ('name', 'rollnumber','email','department','course','yearofpassing')
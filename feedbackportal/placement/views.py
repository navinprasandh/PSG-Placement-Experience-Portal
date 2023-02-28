from django.shortcuts import render
from django.http import HttpResponse
from .models import Carausel 
#from django.views.generic import CreateView
from django.template import loader
from django.http import HttpResponseRedirect
#from .forms import RegisterForm
from django.contrib.auth.models import User


def main(request):
    obj = Carausel.objects.all()
    context = {
        'obj':obj
    }
    return render(request,'main/home.html',context)
  
def detail(request):
    template = loader.get_template('main/detail.html')
    return HttpResponse(template.render())

def about(request):
    return render(request,"main/about.html")
    

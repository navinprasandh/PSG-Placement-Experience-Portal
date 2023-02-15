from django.shortcuts import render
from django.http import HttpResponse
from .models import Carausel 
#from django.views.generic import CreateView
from django.template import loader


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

#def studentview(CreateView):
 #   model = Students
  #  fields = ('name', 'rollnumber','email','department','course','yearofpassing')
from django.shortcuts import render
from django.http import HttpResponse
from .models import Carausel
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
   

def profile(request):
    return render(request,"main/profile.html")
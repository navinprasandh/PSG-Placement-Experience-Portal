from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def placement(request):
    template = loader.get_template('main/homepage.html')
    return HttpResponse(template.render())

def main(request):
    template = loader.get_template('main/home.html')
    return HttpResponse(template.render())

def detail(request):
    template = loader.get_template('main/detail.html')
    return HttpResponse(template.render())
   

def profile(request):
    return render(request,"main/profile.html")
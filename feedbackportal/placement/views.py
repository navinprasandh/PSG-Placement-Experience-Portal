from django.shortcuts import render
from django.http import HttpResponse
from .models import Carausel 
from django.template import loader
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from placement.forms import SignupForm
from placement.models import Student
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

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
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_active = False
            student.save()
            token = get_random_string(length=32)
            subject = 'Activate Your Account'
            message = f'Click this link to activate your account: {request.get_host()}/activate/?token={token}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [student.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return render(request, 'activation_sent.html')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def activate_account(request):
    token = request.GET.get('token')
    try:
        student = Student.objects.get(token=token)
        student.is_active = True
        student.save()
        return render(request, 'activation_successful.html')
    except Student.DoesNotExist:
        return render(request, 'activation_invalid.html')
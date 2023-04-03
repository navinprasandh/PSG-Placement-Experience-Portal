from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Carausel 
from django.template import loader
from django.conf import settings
from .models import *
from .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

class Register(SuccessMessageMixin, CreateView):
	success_url = reverse_lazy('register')
	success_message = 'Account has been sucessfully created! Check your mail and verify your account before signing in.'
	form_class = NewUserSignupForm
	template_name = 'main/register.html'

@login_required
def Profile(request):
	if request.user.is_superuser or request.user.is_staff:
		return redirect('/admin/placement/users/')
	if request.method == 'POST':
		form = UpdateForm(data=request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated!')
			return redirect(reverse_lazy('profile'))
	else:
		form = UpdateForm(instance=request.user)
	context = {
		'form': form,
	}
	return render(request, 'main/formone.html', context)

class Dashboard(LoginRequiredMixin, View):
	login_url = reverse_lazy('login')

	def get(self, request):
		if request.user.is_superuser or request.user.is_staff:
			return redirect(reverse_lazy('admin:login'))
		else:
			context = {
			}
			return render(request, 'main/formone.html', context)
		return redirect(reverse_lazy('login'))


def placement_forms(request):
	round_name = PlacementRound.objects.all()
	form_data = {}
	for i in round_name:
		round_questions = RoundQuestions.objects.filter(placement_round__name=i.name).values('question')
		questions = []
		for j in round_questions:
			questions.append(j['question'])
		form_data[i.name] = questions
	print(form_data)
	return HttpResponse(round_name)


# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.is_active = False
#             student.save()
#             token = get_random_string(length=32)
#             subject = 'Activate Your Account'
#             message = f'Click this link to activate your account: {request.get_host()}/activate/?token={token}'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [student.email]
#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#             return render(request, 'activation_sent.html')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})

# def activate_account(request):
#     token = request.GET.get('token')
#     try:
#         student = Student.objects.get(token=token)
#         student.is_active = True
#         student.save()
#         return render(request, 'activation_successful.html')
#     except Student.DoesNotExist:
#         return render(request, 'activation_invalid.html')

# def student_info(request):
#     stu= StudentForm()
#     if request.method=='POST':
#         stu=StudentForm(request.POST, request.FILES)
#         if stu.is_valid():
#             stu.save()
#         return redirect('home')
#     return render(request, "main/student_info.html", {'stu':stu})
from django.urls import reverse
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
from dynamic_forms.views import DynamicFormMixin
from django.views.generic import TemplateView, DetailView
from django.db.models import Q


def main(request):
    obj = Carausel.objects.all()
    survey = Survey.objects.all()
    survey_ids = []
    for i in survey:
        survey_ids.append(i.id)
    search_query = request.GET.get("search_query")
    if search_query:
        fields = [
            "user__name",
            "user__email",
            "user__roll_number",
            "user__department__name",
            "user__course__name",
            "user__year_of_passing",
            "user__placed_company",
            "survey__topic",
            "response",
        ]
        q_objects = Q()
        for field in fields:
            q_objects |= Q(**{f"{field}__icontains": search_query})
        survey_response = SurveyResponse.objects.filter(q_objects).order_by("user")
    else:
        survey_response = SurveyResponse.objects.all().order_by("user")
    context = {
        "obj": obj,
        "survey": survey_ids,
        "survey_response": survey_response,
    }
    return render(request, "main/home.html", context)


def detail(request):
    template = loader.get_template("main/detail.html")
    return HttpResponse(template.render())


def about(request):
    return render(request, "main/about.html")


class Register(SuccessMessageMixin, CreateView):
    success_url = reverse_lazy("register")
    success_message = "Account has been sucessfully created! Check your mail and verify your account before signing in."
    form_class = NewUserSignupForm
    template_name = "main/register.html"


@login_required
def Profile(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect("/admin/placement/users/")
    if request.method == "POST":
        form = UpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect(reverse_lazy("profile"))
    else:
        is_profile_updated = False
        if (
            request.user.roll_number is None
            or request.user.contact is None
            or request.user.year_of_passing is None
            or request.user.course is None
            or request.user.department is None
            or request.user.placed_company is None
            or request.user.package is None
            or request.user.offer_type is None
            or request.user.profile_pic is None
        ):
            is_profile_updated = False
            messages.warning(
                request, "Please update your profile with all the details to continue!"
            )
        else:
            is_profile_updated = True
        survey = Survey.objects.all()
        """
        Check if the user has already responded to the survey using the user id in SurveyResponse model
            - If yes, then don't show the survey
            - If no, then show the survey
        """
        not_attempted_surveys = []
        for i in survey:
            if not SurveyResponse.objects.filter(
                survey_id=i.id, user=request.user.id
            ).exists():
                not_attempted_surveys.append(i.id)
        form = UpdateForm(instance=request.user)
    context = {
        "form": form,
        "survey": not_attempted_surveys,
        "is_profile_updated": is_profile_updated,
    }
    return render(request, "main/formone.html", context)


class SurveyDetailView(DetailView):
    model = Survey
    pk_url_kwarg = "survey_id"
    template_name = "main/survey/survey_detail.html"


class RespondView(DynamicFormMixin, CreateView):
    model = SurveyResponse
    fields = ["response"]
    template_name = "main/survey/respond.html"

    form_model = Survey
    form_pk_url_kwarg = "survey_id"
    response_form_fk_field = "survey"
    response_field = "response"

    def get_success_url(self):
        msg = "Thank you for your response!"
        messages.success(self.request, msg)
        return reverse("profile")

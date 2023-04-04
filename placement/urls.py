from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', main, name='main'),
    path('detail/', detail, name='detail'),
    path('about/', about, name='about'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name="login"),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', Profile, name="profile"),
    path('survey/<int:survey_id>/response/', RespondView.as_view(), name="survey_respond"),
    path('survey/<int:survey_id>/', SurveyDetailView.as_view(), name="survey_detail"),
]

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', main, name='main'),
    path('detail/', detail, name='detail'),
    path('about/', about, name='about'),
    # path('signin/', signin, name='signin'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name="login"),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', Profile, name="profile"),
    path('round/', placement_forms, name="round"),
    # path('activate/', activate_account, name='activate_account'), 
    # path('studentinfo/', views.student_info, name='studentinfo'),
]

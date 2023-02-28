from django.urls import path
from . import views
from placement.views import signup, activate_account


urlpatterns = [
    path('main/', views.main, name='main'),
    path('detail/', views.detail, name='detail'),
    path('about/', views.about, name='about'),
    path('signup/', signup, name='signup'),
    path('activate/', activate_account, name='activate_account'), 
]

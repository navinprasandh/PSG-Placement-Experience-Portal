from django.urls import path
from . import views



urlpatterns = [
    path('main/', views.main, name='main'),
    path('detail/', views.detail, name='detail'),
    path('about/', views.about, name='about'),
]

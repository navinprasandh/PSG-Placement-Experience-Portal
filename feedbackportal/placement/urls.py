from django.urls import path
from . import views

urlpatterns = [
    path('placement/', views.placement, name='placement'),
    path('main/', views.detail, name='detail'),
]
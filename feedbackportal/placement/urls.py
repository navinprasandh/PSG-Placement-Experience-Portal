from django.urls import path
from . import views



urlpatterns = [
    path('placement/', views.placement, name='placement'),
    path('main/', views.main, name='main'),
    path('detail/', views.detail, name='detail'),
]

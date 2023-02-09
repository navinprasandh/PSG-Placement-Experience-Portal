from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('placement/', views.placement, name='placement'),
    path('main/', views.detail, name='detail'),
]

urlpatterns += staticfiles_urlpatterns()
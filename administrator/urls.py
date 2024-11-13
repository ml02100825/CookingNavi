from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views 

app_name = "administrator"
urlpatterns = [
     path('home/', views.HomeView.as_view(), name='home'),
]
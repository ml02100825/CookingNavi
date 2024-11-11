from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views 

app_name = "account"
urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpPage1View.as_view(), name='signup'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='top'),
]
from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views 

app_name = "account"
urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('', views.IndexView.as_view(), name='top'),
]
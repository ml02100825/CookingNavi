from django.urls import path
from . import  views
from django.contrib.auth import views as auth_views 

app_name = "account"
urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('signup1/', views.SignUpPage1View.as_view(), name='signup1'),
    path('signup2/', views.SignUpPage2View.as_view(), name='signup2'),
    path('signup_completion/', views.CustomSignUpView.as_view(), name='signup_completion'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('username/', views.UsernameView.as_view(), name='username'),
    path('email/', views.EmailView.as_view(), name='email'),
    path('email_henko_ok/', views.EmailOkView.as_view(), name='email_henko_ok'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('password_henko_ok/', views.PasswordOkView.as_view(), name='password_henko_ok'),
    path('', views.IndexView.as_view(), name='top'),
]
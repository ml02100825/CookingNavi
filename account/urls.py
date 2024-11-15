from django.urls import path
from . import  views

app_name = "account"
urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('signup1/', views.SignUpPage1View.as_view(), name='signup1'),
    path('signup2/', views.SignUpPage2View.as_view(), name='signup2'),
    path('signup_completion/', views.CustomSignUpView.as_view(), name='signup_completion'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout_ok/', views.LogoutOkView.as_view(), name='logout_ok'),
    path('', views.IndexView.as_view(), name='top'),
]
from django.urls import path
from . import  views
from .views import LogoutConfirmView
from django.views.generic import TemplateView

app_name = "account"
urlpatterns = [
    path('login/',  views.CustomLoginView.as_view(), name='login'),
    path('signup1/', views.SignUpPage1View.as_view(), name='signup1'),
    path('signup2/', views.SignUpPage2View.as_view(), name='signup2'),
    path('signup_completion/', views.CustomSignUpView.as_view(), name='signup_completion'),
    path('logout/', LogoutConfirmView.as_view(), name='logout'),
    path('logout/ok/', TemplateView.as_view(template_name="logout/logout_ok.html"), name='logout_ok'),
    path('', views.IndexView.as_view(), name='top'),
]
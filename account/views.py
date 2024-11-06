from httprequest import request
from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.views.generic.base import TemplateView, LoginView as BaseLoginView
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginFrom #ログインフォームをimport


class LoginView(BaseLoginView):
    
    template_name='Login.html'

    form_class = LoginFrom
    template_name = "accounts/login.html"
class IndexView(TemplateView):
    
    template_name='top.html'
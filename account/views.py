from django.shortcuts import render

# Create your views here.
# Create your views here.
from django.views.generic.base import TemplateView
from requests import request
from django.contrib.auth import authenticate, login


class LoginView(TemplateView):
    
    template_name='Login.html'
    mailaddress = request.POST["mailaddress"]
    password = request.POST["password"]
    user = authenticate(request, mailaddress = mailaddress, password = password)
    if user is not None:
        login(request, user)
    else:
        pass
class IndexView(TemplateView):
    
    template_name='top.html'
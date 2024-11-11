from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    
    template_name='index.html'

class HomeView(TemplateView):
    template_name='home/home2.html'

class HealthMainView(TemplateView):
    template_name='health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health_selection.html'

class AccountSettingView(TemplateView):
    template_name='account_setting.html'

class AcountSettingView(TemplateView):
    template_name='setting/setting.html'
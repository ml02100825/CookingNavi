from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    
    template_name='index.html'

class HomeView(TemplateView):
    template_name='home/home.html'

class HealthMainView(TemplateView):
    template_name='health_management_main.html'

class HealthSelectionView(TemplateView):
    template_name='health_selection.html'

class SettingView(TemplateView):
    template_name='setting/setting.html'

class AcountSettingView(TemplateView):
    template_name='acount/acount_setting.html'

class FamilyInfoView(TemplateView):
    template_name='kazoku/kazoku.html'

class BodyInfoUpdateView(TemplateView):
    template_name='sintai/sintai_henko.html'

class NotificationSettingView(TemplateView):
    template_name='/.html'

class SubscriptionSettingView(TemplateView):
    template_name='sabusuku/setting/sabusuku_setting.html'